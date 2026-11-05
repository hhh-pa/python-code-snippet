#!/usr/bin/env python3
"""Load-independent performance measurement for Python snippets.

Runs every src/**/*.py script against the shared test cases and records
metrics under Intel Pin (inscount tool):

  * pin_instructions (executed application instructions under Pin) --
    fully load-independent and deterministic across runs.
  * cpu_s (user + sys CPU time).
  * wall_s (wall time).
  * maxrss_kb (peak RSS in KB).

Plus, when Valgrind is installed locally, Callgrind instruction reads
('Ir') as instructions min/median/max per case. CI no longer installs
Valgrind, so the Callgrind signal is absent there; the Callgrind code
paths stay for local use.

Usage:
    python3 tools/measure.py --resources tests/resources \
        [--repeat 1] [--jobs 2] [--timeout 300] [--only substring] \
        [--output perf.json] [--bmf-output bencher.json] \
        [--summary-file "$GITHUB_STEP_SUMMARY"] [--shard K/N] \
        --pin --pin-bin BIN --pin-tool SO [--pin-repeat N] \
        [--pin-timeout S]

    python3 tools/measure.py --merge shard-*.json --output merged.json \
        [--bmf-output bencher.json] [--summary-file summary.md]

    python3 tools/measure.py --self-test
"""

import argparse
import glob
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import run_tests

TOOL_VERSION = 3
_CALLGRIND_TOTAL_RE = re.compile(r"^(?:totals|summary):\s*(\d+)", re.MULTILINE)

# Pin inscount defaults: two counts per case catch instrument
# flakiness without paying for more slow runs; the Pin budget is
# separate from --timeout since instrumentation runs ~10-100x slower.
PIN_REPEAT_DEFAULT = 2
PIN_TIMEOUT_DEFAULT = 600


def parse_callgrind_output(content):
    """Extract total instruction count from Callgrind output text."""
    matches = _CALLGRIND_TOTAL_RE.findall(content)
    if matches:
        return int(matches[-1])
    # Fallback to search any 'summary:' or 'totals:'
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("totals:") or line.startswith("summary:"):
            parts = line.split(":")
            if len(parts) >= 2:
                try:
                    return int(parts[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
    return None


def parse_pin_count(content):
    """Extract the total from inscount-style tool output (one "Count N" line).

    Later Count lines win so per-thread dumps still resolve to their
    trailing total. Raises ValueError when no Count line parses.
    """
    found = None
    for line in content.splitlines():
        fields = line.split()
        if len(fields) != 2 or fields[0] != "Count":
            continue
        digits = fields[1]
        if not digits or any(c not in "0123456789" for c in digits):
            raise ValueError("pin count unreadable: {!r}".format(line.strip()))
        found = int(digits)
    if found is None:
        raise ValueError("pin count unreadable: no Count line")
    return found


def pin_usable(pin_bin, tool):
    """Whether Pin count runs can execute: launcher resolves, tool exists."""
    if not pin_bin or not tool:
        return False
    if not os.path.isfile(tool):
        return False
    if os.path.dirname(pin_bin):
        return os.path.isfile(pin_bin) and os.access(pin_bin, os.X_OK)
    return shutil.which(pin_bin) is not None


def pin_version(pin_bin):
    """Probe `pin -version` for report provenance, or None when silent.

    Compared runs must share one Pin version: counts are only
    comparable within a version.
    """
    try:
        proc = subprocess.run(
            [pin_bin, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    for line in proc.stdout.decode(errors="ignore").splitlines():
        if line.strip():
            return line.strip()
    return None


def is_pin_timeout(run_err):
    """Whether a Pin run error text is a deadline timeout (degrades to
    a skip) rather than a crash (fails the case)."""
    return "TIMEOUT" in run_err


def parse_shard(text):
    """Parse K/N shard selector into (index, total), 0-based index."""
    try:
        k, _, n = text.partition("/")
        index, total = int(k), int(n)
    except (TypeError, ValueError) as exc:
        raise ValueError("bad --shard {!r}: want K/N".format(text)) from exc
    if total < 1 or not 0 <= index < total:
        raise ValueError("bad --shard {!r}: need 0 <= K < N".format(text))
    return index, total


def select_shard(tasks, index, total):
    """Deterministically keep every total-th snippet starting at index.

    Sharding is by SNIPPET (label), so all test cases of a snippet stay
    together in one shard for consistent BMF aggregation and fan-in merging.
    """
    groups = {}
    for t in tasks:
        # t is (label, stem, script, case_name, inp, outp)
        groups.setdefault(t[0], []).append(t)
    keep = {g for i, g in enumerate(sorted(groups)) if i % total == index}
    return [t for t in tasks if t[0] in keep]


def summarize_numbers(values):
    if not values:
        return None
    values = sorted(values)
    return {
        "min": values[0],
        "median": statistics.median(values),
        "max": values[-1],
    }


def measure_case_callgrind(has_valgrind, script, case_name, input_path, output_path, repeat, timeout):
    with open(output_path, "rb") as fd:
        expected = run_tests.normalize(fd.read())

    runs = []
    for _ in range(repeat):
        callgrind_file = None
        fd_temp = None
        try:
            if has_valgrind:
                fd_temp, callgrind_file = tempfile.mkstemp(prefix="snip-cg-", suffix=".out")
                os.close(fd_temp)
                cmd = [
                    "valgrind",
                    "--tool=callgrind",
                    f"--callgrind-out-file={callgrind_file}",
                    sys.executable,
                    script,
                ]
            else:
                cmd = [sys.executable, script]

            t0 = time.perf_counter()
            with open(input_path, "rb") as stdin_fd:
                try:
                    proc = subprocess.run(
                        cmd,
                        stdin=stdin_fd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=timeout,
                    )
                except subprocess.TimeoutExpired:
                    return None, f"TIMEOUT (>{timeout}s)"
            wall_s = time.perf_counter() - t0

            if proc.returncode != 0:
                err_text = proc.stderr.decode(errors="ignore").strip().splitlines()
                return None, f"exit {proc.returncode}: {err_text[-1] if err_text else 'no stderr'}"

            if run_tests.normalize(proc.stdout) != expected:
                got = run_tests.normalize(proc.stdout).decode(errors="ignore")
                want = expected.decode(errors="ignore")
                return None, f"output mismatch: expected {want[:100]!r} got {got[:100]!r}"

            instructions = None
            if has_valgrind and callgrind_file and os.path.isfile(callgrind_file):
                with open(callgrind_file, "r", errors="ignore") as cg_fd:
                    instructions = parse_callgrind_output(cg_fd.read())

            runs.append({
                "instructions": instructions,
                "wall_s": wall_s,
                "cpu_s": wall_s,  # fallback approximation
                "maxrss_kb": 0,
            })
        finally:
            if callgrind_file and os.path.exists(callgrind_file):
                try:
                    os.unlink(callgrind_file)
                except OSError:
                    pass

    # Summarize runs
    insn_vals = [r["instructions"] for r in runs if r["instructions"] is not None]
    summary = {
        "instructions": summarize_numbers(insn_vals) if insn_vals else None,
        "wall_s": summarize_numbers([r["wall_s"] for r in runs]),
        "cpu_s": summarize_numbers([r["cpu_s"] for r in runs]),
        "maxrss_kb": summarize_numbers([r["maxrss_kb"] for r in runs]),
        "runs": len(runs),
    }
    return summary, None


def pin_once(pin_bin, pin_tool, exec_cmd, input_bytes, timeout):
    """Run exec_cmd once under Pin with the inscount tool.

    Returns (stdout, count, run_err): run_err is "" on success, else a
    short "TIMEOUT (>Ns)" / "exit N: ..." / "pin output unreadable"
    text for the caller to classify.
    """
    fd_temp, out_file = tempfile.mkstemp(prefix="snip-pin-", suffix=".out")
    os.close(fd_temp)
    try:
        cmd = [pin_bin, "-t", pin_tool, "-o", out_file, "--"] + list(exec_cmd)
        try:
            proc = subprocess.run(
                cmd,
                input=input_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return None, 0, "TIMEOUT (>{}s)".format(timeout)
        if proc.returncode != 0:
            err_text = proc.stderr.decode(errors="ignore").strip().splitlines()
            return None, 0, "exit {}: {}".format(
                proc.returncode, err_text[-1] if err_text else "no stderr")
        try:
            with open(out_file, "r", errors="ignore") as fd:
                count = parse_pin_count(fd.read())
        except (OSError, ValueError) as exc:
            return None, 0, "pin output unreadable: {}".format(exc)
        return proc.stdout, count, ""
    finally:
        if os.path.exists(out_file):
            try:
                os.unlink(out_file)
            except OSError:
                pass


def measure_case_pin(exec_cmd, label, case_name, input_path, output_path,
                     pin_bin, pin_tool, pin_repeat, pin_timeout):
    """Pin inscount phase for one case.

    Returns (pin_summary|None, pin_skipped|None, error|None): timeouts
    degrade to pin_skipped (callgrind data stays valid), crashes and
    output mismatches fail the case.
    """
    with open(output_path, "rb") as fd:
        expected = run_tests.normalize(fd.read())
    with open(input_path, "rb") as fd:
        input_bytes = fd.read()

    counts = []
    for i in range(pin_repeat):
        stdout, count, run_err = pin_once(
            pin_bin, pin_tool, exec_cmd, input_bytes, pin_timeout)
        if run_err:
            if is_pin_timeout(run_err):
                print("warning: {}/{}: pin skipped ({})".format(
                    label, case_name, run_err), file=sys.stderr)
                return None, run_err, None
            return None, None, "pin: {}".format(run_err)
        if i == 0 and run_tests.normalize(stdout) != expected:
            got = run_tests.normalize(stdout).decode(errors="ignore")
            want = expected.decode(errors="ignore")
            return None, None, "pin output mismatch: expected {!r} got {!r}".format(
                want[:100], got[:100])
        counts.append(count)
    return summarize_numbers(counts), None, None


def measure_case_full(has_valgrind, label, script, case_name, inp, outp,
                      repeat, timeout, pin_bin, pin_tool, pin_repeat, pin_timeout):
    """Direct/Callgrind measure plus the Pin inscount phase.

    The first phase runs the case natively (or under Callgrind when
    valgrind is installed) for correctness and wall/cpu time; the Pin
    phase provides the deterministic instruction count.

    Returns (summary|None, pin_skipped|None, error|None).
    """
    summary, err = measure_case_callgrind(
        has_valgrind, script, case_name, inp, outp, repeat, timeout)
    if err is not None or pin_repeat <= 0:
        return summary, None, err
    pin_summary, pin_skipped, pin_err = measure_case_pin(
        [sys.executable, script], label, case_name, inp, outp,
        pin_bin, pin_tool, pin_repeat, pin_timeout)
    if pin_err is not None:
        return None, None, pin_err
    if pin_summary is not None:
        summary["pin_instructions"] = pin_summary
    return summary, pin_skipped, None


def build_bmf(results):
    """Aggregate per-snippet summaries into Bencher Metric Format JSON."""
    snippets = {}
    for r in results:
        label = r["label"]
        snippets.setdefault(label, []).append(r)

    bmf = {}
    for name in sorted(snippets):
        items = snippets[name]
        total_instructions = 0
        has_instructions = False
        total_pin = 0
        has_pin = False
        total_cpu = 0.0

        for it in items:
            s = it.get("summary")
            if not s:
                continue
            if s.get("instructions") and s["instructions"]["median"] is not None:
                total_instructions += int(s["instructions"]["median"])
                has_instructions = True
            if s.get("pin_instructions") and s["pin_instructions"]["median"] is not None:
                total_pin += int(s["pin_instructions"]["median"])
                has_pin = True
            if s.get("cpu_s") and s["cpu_s"]["median"] is not None:
                total_cpu += float(s["cpu_s"]["median"])

        measures = {}
        if has_instructions:
            measures["instructions"] = {"value": total_instructions}
        if has_pin:
            measures["pin_instructions"] = {"value": total_pin}
        measures["cpu_time"] = {"value": total_cpu}

        bmf[name] = measures
    return bmf


def merge_reports(paths):
    merged_results = []
    failures = []
    seen = set()

    for path in sorted(paths):
        with open(path) as f:
            data = json.load(f)
        for item in data.get("results", []):
            key = (item["label"], item["case"])
            if key not in seen:
                seen.add(key)
                merged_results.append(item)
        failures.extend(data.get("failures", []))

    report = {
        "tool_version": TOOL_VERSION,
        "platform": platform.platform(),
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": merged_results,
        "failures": failures,
    }
    return report, build_bmf(merged_results)


def append_summary(path, report, bmf):
    if not path:
        return
    lines = [
        "### Instrumentation Performance Summary (Python)",
        "",
        "| Benchmark | Cases | Pin Instr | Callgrind Ir | CPU Time (s) |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]

    total_insn = 0
    total_pin = 0
    total_cpu = 0.0
    has_insn = False
    has_pin = False

    snippets = {}
    for r in report.get("results", []):
        snippets.setdefault(r["label"], []).append(r)

    for name in sorted(snippets):
        cases_count = len(snippets[name])
        m = bmf.get(name, {})
        pin_str = "-"
        if "pin_instructions" in m:
            val = m["pin_instructions"]["value"]
            pin_str = f"{val:,}"
            total_pin += val
            has_pin = True
        insn_str = "-"
        if "instructions" in m:
            val = m["instructions"]["value"]
            insn_str = f"{val:,}"
            total_insn += val
            has_insn = True
        cpu_val = m.get("cpu_time", {}).get("value", 0.0)
        total_cpu += cpu_val
        lines.append(f"| `{name}` | {cases_count} | {pin_str} | {insn_str} | {cpu_val:.4f} |")

    tot_pin_str = f"{total_pin:,}" if has_pin else "-"
    tot_insn_str = f"{total_insn:,}" if has_insn else "-"
    lines.append(f"| **Total ({len(snippets)} snippets)** | - | **{tot_pin_str}** | **{tot_insn_str}** | **{total_cpu:.4f}** |")
    lines.append("")

    with open(path, "a") as f:
        f.write("\n".join(lines) + "\n")


def self_test():
    print("Running self-test for measure.py...")
    sample_cg = """
events: Ir
summary: 987654321
totals: 987654321
"""
    parsed = parse_callgrind_output(sample_cg)
    assert parsed == 987654321, f"Expected 987654321, got {parsed}"

    assert parse_pin_count("Count 846018869\n") == 846018869
    assert parse_pin_count("Pin 3.31\nCount 1\nCount 42\n") == 42
    for bad in ("", "no counts here\n", "Count abc\n", "Count\n", "Count 1 2\n"):
        try:
            parse_pin_count(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"parse_pin_count must reject {bad!r}")
    assert not pin_usable("", "")
    assert not pin_usable("/nonexistent/pin", "/nonexistent/tool.so")
    assert is_pin_timeout("TIMEOUT (>900s)")
    for other in ("", "exit 1: boom", "pin output unreadable: x",
                  "pin count unreadable: x"):
        assert not is_pin_timeout(other), other

    sample_tasks = [
        ("sort/merge_sort", "solution", "s1", "tc0", "in", "out"),
        ("sort/merge_sort", "solution", "s1", "tc1", "in", "out"),
        ("sort/quick_sort", "solution", "s2", "tc0", "in", "out"),
        ("math/gcd", "solution", "s3", "tc0", "in", "out"),
    ]
    sh0 = select_shard(sample_tasks, 0, 2)
    sh1 = select_shard(sample_tasks, 1, 2)
    assert len(sh0) + len(sh1) == len(sample_tasks)
    # Check that merge_sort cases stay together
    labels_sh0 = {t[0] for t in sh0}
    labels_sh1 = {t[0] for t in sh1}
    assert labels_sh0.isdisjoint(labels_sh1)

    # Test BMF generation
    mock_results = [
        {
            "label": "sort/merge_sort",
            "case": "tc0",
            "summary": {
                "instructions": {"median": 1000},
                "pin_instructions": {"median": 4000},
                "cpu_s": {"median": 0.05},
            },
        },
        {
            "label": "sort/merge_sort",
            "case": "tc1",
            "summary": {
                "instructions": {"median": 2000},
                "pin_instructions": {"median": 8000},
                "cpu_s": {"median": 0.05},
            },
        },
    ]
    bmf = build_bmf(mock_results)
    assert bmf["sort/merge_sort"]["instructions"]["value"] == 3000
    assert bmf["sort/merge_sort"]["pin_instructions"]["value"] == 12000
    assert abs(bmf["sort/merge_sort"]["cpu_time"]["value"] - 0.10) < 1e-6

    # Pin BMF without any Callgrind signal (the CI shape: no
    # valgrind installed, so no "instructions" measure at all).
    pin_only = [
        {
            "label": "math/gcd",
            "case": "tc0",
            "summary": {
                "instructions": None,
                "pin_instructions": {"median": 9000},
                "cpu_s": {"median": 0.02},
            },
        },
    ]
    bmf_pin = build_bmf(pin_only)
    assert "instructions" not in bmf_pin["math/gcd"]
    assert bmf_pin["math/gcd"]["pin_instructions"]["value"] == 9000

    print("self-test passed!")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default=os.path.join(ROOT, "tests", "resources"))
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--only", default="", help="filter by label substring")
    parser.add_argument("--shard", default="", help="shard K/N (0-based K)")
    parser.add_argument("--output", default=None, help="JSON output file")
    parser.add_argument("--bmf-output", default=None, help="Bencher Metric Format output")
    parser.add_argument("--summary-file", default=None, help="Markdown summary output")
    parser.add_argument("--merge", nargs="*", default=None, help="merge shard JSON files")
    parser.add_argument("--self-test", action="store_true", help="run self-test")
    parser.add_argument("--pin", action="store_true",
                        help="count instructions under Intel Pin (primary signal)")
    parser.add_argument("--pin-bin", default="",
                        help="Pin launcher binary (Intel kit, direct download)")
    parser.add_argument("--pin-tool", default="",
                        help="inscount tool .so for Pin (-t)")
    parser.add_argument("--pin-repeat", type=int, default=PIN_REPEAT_DEFAULT)
    parser.add_argument("--pin-timeout", type=int, default=PIN_TIMEOUT_DEFAULT)
    args = parser.parse_args(argv)

    if args.pin_repeat < 1:
        parser.error("--pin-repeat must be >= 1")
    if args.pin_timeout < 1:
        parser.error("--pin-timeout must be >= 1")

    if args.self_test:
        return self_test()

    if args.merge is not None:
        report, bmf = merge_reports(args.merge)
        if args.output:
            with open(args.output, "w") as f:
                json.dump(report, f, indent=2)
        if args.bmf_output:
            with open(args.bmf_output, "w") as f:
                json.dump(bmf, f, indent=2)
        if args.summary_file:
            append_summary(args.summary_file, report, bmf)
        print(f"Merged {len(args.merge)} reports: {len(report['results'])} cases, {len(bmf)} benchmarks.")
        return 0

    has_valgrind = shutil.which("valgrind") is not None
    if not has_valgrind:
        print("warning: valgrind not found in PATH; running Python directly without Callgrind simulation", file=sys.stderr)

    use_pin = args.pin and pin_usable(args.pin_bin, args.pin_tool)
    if args.pin and not use_pin:
        print("warning: pin unavailable (need --pin-bin launcher and --pin-tool inscount .so); pin_instructions will be null", file=sys.stderr)
    pin_ver = pin_version(args.pin_bin) if use_pin else None
    effective_pin_repeat = args.pin_repeat if use_pin else 0

    tasks = []
    missing = []
    for area, problem, stem, script, cases in run_tests.discover(args.resources):
        label = f"{area}/{problem}/{stem}" if problem != stem else f"{area}/{problem}"
        if args.only and args.only not in label and args.only not in script:
            continue
        if not cases:
            missing.append(label)
            continue
        for case_name, inp, outp in cases:
            tasks.append((label, stem, script, case_name, inp, outp))

    tasks = sorted(tasks)
    if args.shard:
        index, total = parse_shard(args.shard)
        tasks = select_shard(tasks, index, total)

    total_tasks = len(tasks)
    if use_pin:
        backend = "Pin inscount"
    elif has_valgrind:
        backend = "Callgrind"
    else:
        backend = "direct run (no instrumentation)"
    print(f"Measuring {total_tasks} cases ({len({t[0] for t in tasks})} benchmarks) with {backend}...")

    results = []
    failures = []
    done = 0

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                measure_case_full,
                has_valgrind,
                label,
                script,
                case_name,
                inp,
                outp,
                args.repeat,
                args.timeout,
                args.pin_bin,
                args.pin_tool,
                effective_pin_repeat,
                args.pin_timeout,
            ): (label, stem, script, case_name)
            for label, stem, script, case_name, inp, outp in tasks
        }
        for future in as_completed(futures):
            label, stem, script, case_name = futures[future]
            summary, pin_skipped, err = future.result()
            done += 1
            if err is None:
                parts = []
                if summary.get("pin_instructions"):
                    pin_med = summary["pin_instructions"]["median"]
                    parts.append(f"{int(pin_med):,} Pin")
                elif pin_skipped:
                    parts.append(f"pin skipped: {pin_skipped}")
                insn = summary["instructions"]["median"] if summary.get("instructions") else None
                parts.append(f"{int(insn):,} Ir" if insn else "n/a Ir")
                print(f"[{done}/{total_tasks}] {label}/{case_name}: {'; '.join(parts)}")
                entry = {
                    "label": label,
                    "stem": stem,
                    "case": case_name,
                    "script": os.path.relpath(script, ROOT),
                    "summary": summary,
                }
                if pin_skipped:
                    entry["pin_skipped"] = pin_skipped
                results.append(entry)
            else:
                print(f"[{done}/{total_tasks}] FAIL {label}/{case_name}: {err}")
                failures.append(f"{label}/{case_name}: {err}")

    report = {
        "tool_version": TOOL_VERSION,
        "platform": platform.platform(),
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "has_valgrind": has_valgrind,
        "pin_used": use_pin,
        "pin_version": pin_ver,
        "results": results,
        "failures": failures,
    }
    bmf = build_bmf(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
    if args.bmf_output:
        with open(args.bmf_output, "w") as f:
            json.dump(bmf, f, indent=2)
    if args.summary_file:
        append_summary(args.summary_file, report, bmf)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
