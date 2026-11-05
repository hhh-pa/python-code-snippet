#!/usr/bin/env python3
"""Load-independent performance measurement for Python snippets.

Runs every src/**/*.py script against the shared test cases and records
metrics under Intel Pin (inscount tool):

  * pin_instructions (executed application instructions under Pin) --
    fully load-independent and deterministic across runs.
  * allocated_bytes (cumulative libc allocation in the same Pin run,
    via the LD_PRELOAD alloc shim) -- the memory signal. It includes
    Pin's own JIT/VM allocations, so like pin_instructions it is only
    comparable within one Pin version.
  * cpu_s (user + sys CPU time, timed phase only).
  * wall_s (wall time, timed phase only).
  * maxrss_kb (peak RSS in KB, timed phase only).

Pin-only mode (--repeat 0, needs --pin): skips the native timed phase
entirely, so each case is measured ONCE under Pin; correctness still
gates on the instrumented run's stdout. Timed signals stay null and
the renderers print "-" / omit BMF rows instead of zeros. Peak RSS is
never read from instrumented runs -- Pin's own footprint pollutes it.

Plus, when Valgrind is installed locally, Callgrind instruction reads
('Ir') as instructions min/median/max per case. CI no longer installs
Valgrind, so the Callgrind signal is absent there; the Callgrind code
paths stay for local use.

Usage:
    python3 tools/measure.py --resources tests/resources \
        [--repeat 0] [--jobs 2] [--only substring] \
        [--output perf.json] [--bmf-output bencher.json] \
        [--summary-file "$GITHUB_STEP_SUMMARY"] [--shard K/N] \
        --pin --pin-bin BIN --pin-tool SO [--pin-repeat N] \
        [--pin-timeout S] [--time-bin BIN] [--label-style python|snip]

Timed repeats run under GNU time (required when --repeat > 0) for
real cpu_s/maxrss_kb. --label-style snip renders area/problem
labels so head-to-head runs key identically to
clojure-code-snippet.

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

TOOL_VERSION = 4
_CALLGRIND_TOTAL_RE = re.compile(r"^(?:totals|summary):\s*(\d+)", re.MULTILINE)

# LD_PRELOAD alloc-shim channel: the shim's destructor prints exactly
# one "snip_alloc_total_bytes=N" line on the child's stderr.
ALLOC_MARKER = "snip_alloc_total_bytes="
ALLOC_SHIM_SRC = os.path.join(
    ROOT, "scripts", "ci", "instrumentation", "allocshim.c")

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


def resolve_time_bin(explicit):
    """Resolve a GNU time binary, or None when unusable.

    Prefers the explicit path, else "time" from PATH. Rejects BSD
    time (macOS): only GNU time supports -f/-o. Returns the binary
    path, or None with no side effects.
    """
    candidates = [explicit] if explicit else []
    found = shutil.which("time")
    if found and found not in candidates:
        candidates.append(found)
    for cand in candidates:
        try:
            proc = subprocess.run(
                [cand, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        out = (proc.stdout + proc.stderr).decode(errors="ignore")
        if proc.returncode == 0 and "GNU" in out:
            return cand
    return None


def parse_time_output(content):
    """Parse GNU time -f "%U %S %M" output.

    Returns (cpu_seconds, maxrss_kb): user+sys CPU time and peak
    resident set. Raises ValueError when the line is missing or
    malformed.
    """
    for line in content.splitlines():
        fields = line.split()
        if len(fields) != 3:
            continue
        try:
            cpu = float(fields[0]) + float(fields[1])
            rss = int(fields[2])
        except ValueError:
            continue
        return cpu, rss
    raise ValueError("time output unreadable: no '%U %S %M' line")


def case_label(area, problem, stem, style):
    """Render a case label for a suite's key convention.

    "python" keeps this repo's labels ("area/problem/stem" unless
    the stem repeats the problem); "snip" renders area/problem so
    head-to-head runs key identically to clojure-code-snippet
    (whose stem travels separately), making instruction and RSS
    medians directly comparable case by case.
    """
    if style == "snip":
        return "{}/{}".format(area, problem)
    if problem != stem:
        return "{}/{}/{}".format(area, problem, stem)
    return "{}/{}".format(area, problem)


def parse_alloc_total(content):
    """Extract the alloc shim's total from child stderr text.

    The stderr channel is shared with the application, so malformed
    marker lines are skipped (an app echoing the marker cannot break
    the parse) and the last valid total wins. Raises ValueError when
    no marker line parses.
    """
    found = None
    for line in content.splitlines():
        text = line.strip()
        if not text.startswith(ALLOC_MARKER):
            continue
        digits = text[len(ALLOC_MARKER):]
        if digits and all(c in "0123456789" for c in digits):
            found = int(digits)
    if found is None:
        raise ValueError(
            "alloc-shim total unreadable: no snip_alloc_total_bytes line")
    return found


def ensure_alloc_shim():
    """Build the LD_PRELOAD allocation-counting shim on demand.

    Compiles scripts/ci/instrumentation/allocshim.c with cc into a
    fresh temp dir and returns the .so path. Raises RuntimeError when
    the platform has no LD_PRELOAD (non-Linux), no C compiler, or the
    build fails.
    """
    if not sys.platform.startswith("linux"):
        raise RuntimeError("needs Linux (LD_PRELOAD)")
    cc = shutil.which("cc") or shutil.which("gcc")
    if cc is None:
        raise RuntimeError("needs a C compiler (cc not found)")
    if not os.path.isfile(ALLOC_SHIM_SRC):
        raise RuntimeError("shim source missing at {}".format(ALLOC_SHIM_SRC))
    build_dir = tempfile.mkdtemp(prefix="snip-alloc-shim-")
    out = os.path.join(build_dir, "alloc_shim.so")
    try:
        proc = subprocess.run(
            [cc, "-shared", "-fPIC", "-O2", "-o", out, ALLOC_SHIM_SRC, "-ldl"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError("build failed: {}".format(exc))
    if proc.returncode != 0:
        tail = proc.stderr.decode(errors="ignore").strip().splitlines()
        raise RuntimeError("build failed: {}".format(
            tail[-1] if tail else "cc exit {}".format(proc.returncode)))
    return out


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


def measure_case_callgrind(has_valgrind, time_bin, script, case_name, input_path, output_path, repeat, timeout):
    with open(output_path, "rb") as fd:
        expected = run_tests.normalize(fd.read())

    runs = []
    for _ in range(repeat):
        callgrind_file = None
        time_file = None
        fd_temp = None
        try:
            if has_valgrind:
                fd_temp, callgrind_file = tempfile.mkstemp(prefix="snip-cg-", suffix=".out")
                os.close(fd_temp)
                inner = [
                    "valgrind",
                    "--tool=callgrind",
                    f"--callgrind-out-file={callgrind_file}",
                    sys.executable,
                    script,
                ]
            else:
                inner = [sys.executable, script]
            fd_temp, time_file = tempfile.mkstemp(prefix="snip-time-", suffix=".out")
            os.close(fd_temp)
            cmd = [time_bin, "-f", "%U %S %M", "-o", time_file] + inner

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
            try:
                with open(time_file, "r", errors="ignore") as tm_fd:
                    cpu_s, maxrss_kb = parse_time_output(tm_fd.read())
            except (OSError, ValueError) as exc:
                return None, "time output unreadable: {}".format(exc)

            runs.append({
                "instructions": instructions,
                "wall_s": wall_s,
                "cpu_s": cpu_s,
                "maxrss_kb": maxrss_kb,
            })
        finally:
            for path in (callgrind_file, time_file):
                if path and os.path.exists(path):
                    try:
                        os.unlink(path)
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


def pin_once(pin_bin, pin_tool, exec_cmd, input_bytes, timeout, alloc_shim=None):
    """Run exec_cmd once under Pin with the inscount tool.

    When alloc_shim names a built shim .so, it is LD_PRELOADed into
    the same run, so the one instrumented execution yields both the
    instruction count and the cumulative allocated bytes.

    Returns (stdout, count, alloc_bytes|None, run_err): run_err is ""
    on success, else a short "TIMEOUT (>Ns)" / "exit N: ..." /
    "pin output unreadable" / "pin alloc output unreadable" text for
    the caller to classify. A missing shim total after a successful
    exit fails the case: the harness is broken, not the snippet, and
    silently dropping a tracked measure is worse than a red case.
    """
    fd_temp, out_file = tempfile.mkstemp(prefix="snip-pin-", suffix=".out")
    os.close(fd_temp)
    try:
        cmd = [pin_bin, "-t", pin_tool, "-o", out_file, "--"] + list(exec_cmd)
        if sys.platform.startswith("linux") and shutil.which("setarch"):
            # Fixed address layout: keeps CPython's mmaps clear of
            # Pin's reserved region under ASLR, mirroring the JVM legs.
            cmd = ["setarch", "-R"] + cmd
        env = None
        if alloc_shim:
            env = dict(os.environ)
            prev = env.get("LD_PRELOAD")
            env["LD_PRELOAD"] = alloc_shim if not prev else alloc_shim + ":" + prev
        try:
            proc = subprocess.run(
                cmd,
                input=input_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return None, 0, None, "TIMEOUT (>{}s)".format(timeout)
        if proc.returncode != 0:
            err_text = proc.stderr.decode(errors="ignore").strip().splitlines()
            return None, 0, None, "exit {}: {}".format(
                proc.returncode, err_text[-1] if err_text else "no stderr")
        try:
            with open(out_file, "r", errors="ignore") as fd:
                count = parse_pin_count(fd.read())
        except (OSError, ValueError) as exc:
            return None, 0, None, "pin output unreadable: {}".format(exc)
        alloc_bytes = None
        if alloc_shim:
            try:
                alloc_bytes = parse_alloc_total(
                    proc.stderr.decode(errors="ignore"))
            except ValueError as exc:
                return None, 0, None, "pin alloc output unreadable: {}".format(exc)
        return proc.stdout, count, alloc_bytes, ""
    finally:
        if os.path.exists(out_file):
            try:
                os.unlink(out_file)
            except OSError:
                pass


def measure_case_pin(exec_cmd, label, case_name, input_path, output_path,
                     pin_bin, pin_tool, pin_repeat, pin_timeout, alloc_shim=None):
    """Pin inscount (+ alloc shim) phase for one case.

    Returns (signals|None, pin_skipped|None, error|None): signals maps
    "pin_instructions" and, when the shim ran, "allocated_bytes" to
    min/median/max summaries. Timeouts degrade to pin_skipped (timed
    data, if any, stays valid); crashes and output mismatches fail
    the case.
    """
    with open(output_path, "rb") as fd:
        expected = run_tests.normalize(fd.read())
    with open(input_path, "rb") as fd:
        input_bytes = fd.read()

    counts = []
    allocs = []
    for i in range(pin_repeat):
        stdout, count, alloc_bytes, run_err = pin_once(
            pin_bin, pin_tool, exec_cmd, input_bytes, pin_timeout, alloc_shim)
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
        if alloc_bytes is not None:
            allocs.append(alloc_bytes)
    signals = {"pin_instructions": summarize_numbers(counts)}
    if allocs:
        signals["allocated_bytes"] = summarize_numbers(allocs)
    return signals, None, None


def measure_case_full(has_valgrind, time_bin, label, script, case_name, inp, outp,
                      repeat, timeout, pin_bin, pin_tool, pin_repeat, pin_timeout,
                      alloc_shim=None):
    """Direct/Callgrind measure plus the Pin inscount phase.

    The first phase runs the case natively (or under Callgrind when
    valgrind is installed) for correctness and wall/cpu time; the Pin
    phase provides the deterministic instruction count. With
    --repeat 0 (pin-only) the first phase is skipped entirely -- no
    native run, no valgrind -- correctness gates on the first Pin
    run, and timed signals stay None.

    Returns (summary|None, pin_skipped|None, error|None).
    """
    if repeat > 0:
        summary, err = measure_case_callgrind(
            has_valgrind, time_bin, script, case_name, inp, outp, repeat, timeout)
        if err is not None or pin_repeat <= 0:
            return summary, None, err
    else:
        summary = {
            "instructions": None,
            "wall_s": None,
            "cpu_s": None,
            "maxrss_kb": None,
            "runs": 0,
        }
    signals, pin_skipped, pin_err = measure_case_pin(
        [sys.executable, script], label, case_name, inp, outp,
        pin_bin, pin_tool, pin_repeat, pin_timeout, alloc_shim)
    if pin_err is not None:
        return None, None, pin_err
    if signals is not None:
        summary.update(signals)
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
        total_alloc = 0
        has_alloc = False
        total_cpu = 0.0
        has_cpu = False

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
            if s.get("allocated_bytes") and s["allocated_bytes"]["median"] is not None:
                total_alloc += int(s["allocated_bytes"]["median"])
                has_alloc = True
            if s.get("cpu_s") and s["cpu_s"]["median"] is not None:
                total_cpu += float(s["cpu_s"]["median"])
                has_cpu = True

        measures = {}
        if has_instructions:
            measures["instructions"] = {"value": total_instructions}
        if has_pin:
            measures["pin_instructions"] = {"value": total_pin}
        if has_alloc:
            measures["allocated_bytes"] = {"value": total_alloc}
        # Pin-only summaries have no timed phase: no cpu_time row at
        # all, never a zero one.
        if has_cpu:
            measures["cpu_time"] = {"value": total_cpu}

        # A snippet whose cases all pin-skipped in pin-only mode has
        # no signal to track; leaving it out beats an empty entry.
        if not measures:
            continue
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
        "| Benchmark | Cases | Pin Instr | Allocated (B) | Callgrind Ir | CPU Time (s) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    total_insn = 0
    total_pin = 0
    total_alloc = 0
    total_cpu = 0.0
    has_insn = False
    has_pin = False
    has_alloc = False
    has_cpu = False

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
        alloc_str = "-"
        if "allocated_bytes" in m:
            val = m["allocated_bytes"]["value"]
            alloc_str = f"{val:,}"
            total_alloc += val
            has_alloc = True
        insn_str = "-"
        if "instructions" in m:
            val = m["instructions"]["value"]
            insn_str = f"{val:,}"
            total_insn += val
            has_insn = True
        cpu_str = "-"
        if "cpu_time" in m:
            cpu_val = m["cpu_time"]["value"]
            cpu_str = f"{cpu_val:.4f}"
            total_cpu += cpu_val
            has_cpu = True
        lines.append(f"| `{name}` | {cases_count} | {pin_str} | {alloc_str} | {insn_str} | {cpu_str} |")

    tot_pin_str = f"{total_pin:,}" if has_pin else "-"
    tot_alloc_str = f"{total_alloc:,}" if has_alloc else "-"
    tot_insn_str = f"{total_insn:,}" if has_insn else "-"
    tot_cpu_str = f"{total_cpu:.4f}" if has_cpu else "-"
    lines.append(f"| **Total ({len(snippets)} snippets)** | - | **{tot_pin_str}** | **{tot_alloc_str}** | **{tot_insn_str}** | **{tot_cpu_str}** |")
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

    assert parse_time_output("0.12 0.03 15236\n") == (0.15, 15236)
    assert parse_time_output("noise\n1.00 0.00 8192\n") == (1.0, 8192)
    for bad in ("", "no numbers here\n", "0.1 0.2\n", "a b c\n", "1 2 3 4\n"):
        try:
            parse_time_output(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("parse_time_output must reject {!r}".format(bad))

    assert case_label("sort", "bubble_sort", "solution", "python") == "sort/bubble_sort/solution"
    assert case_label("sort", "bubble_sort", "solution", "snip") == "sort/bubble_sort"
    assert case_label("math", "gcd", "gcd", "python") == "math/gcd"
    assert case_label("math", "gcd", "gcd", "snip") == "math/gcd"

    # Alloc-shim totals: last valid marker wins, malformed marker
    # lines are skipped (stderr is shared with the app).
    assert parse_alloc_total("hi\nsnip_alloc_total_bytes=123\n") == 123
    assert parse_alloc_total(
        "snip_alloc_total_bytes=1\nsnip_alloc_total_bytes=42\n") == 42
    assert parse_alloc_total(
        "snip_alloc_total_bytes=oops\nsnip_alloc_total_bytes=7\n") == 7
    for bad in ("", "no marker here\n", "snip_alloc_total_bytes=\n",
                "snip_alloc_total_bytes=-1\n", "snip_alloc_total_bytes=1.5\n",
                "snip_alloc_total_bytes=oops\n"):
        try:
            parse_alloc_total(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"parse_alloc_total must reject {bad!r}")

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

    # Pin-only shape (--repeat 0): no timed phase, so no cpu_time
    # row at all (never a zero one); allocated_bytes sits next to
    # pin_instructions; an all-skipped snippet stays out of BMF.
    pin_only_nocpu = [
        {
            "label": "math/gcd",
            "case": "tc0",
            "summary": {
                "instructions": None,
                "pin_instructions": {"median": 9000},
                "allocated_bytes": {"median": 4096},
                "cpu_s": None,
                "runs": 0,
            },
        },
    ]
    bmf_nocpu = build_bmf(pin_only_nocpu)
    assert "cpu_time" not in bmf_nocpu["math/gcd"]
    assert "instructions" not in bmf_nocpu["math/gcd"]
    assert bmf_nocpu["math/gcd"]["pin_instructions"]["value"] == 9000
    assert bmf_nocpu["math/gcd"]["allocated_bytes"]["value"] == 4096
    assert build_bmf([
        {"label": "math/gcd", "case": "tc0",
         "summary": {"instructions": None, "cpu_s": None, "runs": 0}},
    ]) == {}

    # Summary render: pin-only rows show "-" for CPU and the
    # Allocated column; timed rows still show the cpu value.
    fd_temp, tmppath = tempfile.mkstemp(prefix="snip-sum-", suffix=".md")
    os.close(fd_temp)
    try:
        append_summary(tmppath, {"results": pin_only_nocpu}, bmf_nocpu)
        with open(tmppath) as fd:
            pin_text = fd.read()
    finally:
        os.unlink(tmppath)
    assert "Allocated (B)" in pin_text
    assert "| `math/gcd` | 1 | 9,000 | 4,096 | - | - |" in pin_text, pin_text
    fd_temp, tmppath = tempfile.mkstemp(prefix="snip-sum-", suffix=".md")
    os.close(fd_temp)
    try:
        append_summary(tmppath, {"results": mock_results}, bmf)
        with open(tmppath) as fd:
            timed_text = fd.read()
    finally:
        os.unlink(tmppath)
    assert "| `sort/merge_sort` | 2 | 12,000 | - | 3,000 | 0.1000 |" in timed_text, timed_text

    # Alloc-shim build + smoke (Linux only: LD_PRELOAD interposition
    # has no macOS equivalent).
    if sys.platform.startswith("linux"):
        shim = ensure_alloc_shim()
        assert os.path.isfile(shim), shim
        env = dict(os.environ)
        prev = env.get("LD_PRELOAD")
        env["LD_PRELOAD"] = shim if not prev else shim + ":" + prev
        proc = subprocess.run(
            [sys.executable, "-c", "print('hi')"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            env=env,
        )
        assert proc.returncode == 0, proc.stderr.decode(errors="ignore")
        total = parse_alloc_total(proc.stderr.decode(errors="ignore"))
        assert total > 0, total
    else:
        print("(skipping alloc-shim build test: needs Linux)")

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
    parser.add_argument("--no-alloc-shim", action="store_true",
                        help="skip the LD_PRELOAD alloc shim: Pin counts instructions only, no allocated_bytes")
    parser.add_argument("--time-bin", default="",
                        help="GNU time binary for the timed phase (default: auto)")
    parser.add_argument("--label-style", default="python", choices=("python", "snip"),
                        help="snip renders area/problem labels for h2h key alignment")
    args = parser.parse_args(argv)

    if args.pin_repeat < 1:
        parser.error("--pin-repeat must be >= 1")
    if args.pin_timeout < 1:
        parser.error("--pin-timeout must be >= 1")
    if args.repeat < 0:
        parser.error("--repeat must be >= 0")

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
    if not has_valgrind and args.repeat > 0:
        print("warning: valgrind not found in PATH; running Python directly without Callgrind simulation", file=sys.stderr)
    time_bin = resolve_time_bin(args.time_bin)
    if args.repeat > 0 and time_bin is None:
        parser.error("need GNU time for the timed phase (cpu_s/maxrss_kb); install time or pass --time-bin")

    use_pin = args.pin and pin_usable(args.pin_bin, args.pin_tool)
    if args.pin and not use_pin:
        print("warning: pin unavailable (need --pin-bin launcher and --pin-tool inscount .so); pin_instructions will be null", file=sys.stderr)
    if args.repeat == 0 and not use_pin:
        parser.error("--repeat 0 skips the timed phase, so it needs --pin (pin-only mode)")
    pin_ver = pin_version(args.pin_bin) if use_pin else None
    effective_pin_repeat = args.pin_repeat if use_pin else 0

    alloc_shim = None
    if use_pin and not args.no_alloc_shim:
        try:
            alloc_shim = ensure_alloc_shim()
        except RuntimeError as exc:
            print("warning: alloc shim unavailable ({}); allocated_bytes will be null".format(exc), file=sys.stderr)

    tasks = []
    missing = []
    for area, problem, stem, script, cases in run_tests.discover(args.resources):
        label = case_label(area, problem, stem, args.label_style)
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
                time_bin,
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
                alloc_shim,
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
                    if summary.get("allocated_bytes"):
                        alloc_med = summary["allocated_bytes"]["median"]
                        parts.append(f"{int(alloc_med):,}B alloc")
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
                    "ok": True,
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
        "alloc_shim_used": alloc_shim is not None,
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
