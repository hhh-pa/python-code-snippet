#!/usr/bin/env python3
"""Load-independent Callgrind performance measurement for Python snippets.

Each case runs twice per repeat: once natively under GNU time (stdout
gate plus wall/cpu/RSS) and once under Valgrind Callgrind (instruction
count), mirroring the clojure twin's lean recipe:

  * callgrind_instructions (simulated instruction reads 'Ir') --
    fully load-independent and deterministic across runs.
  * cpu_s (user + sys CPU time from GNU time).
  * wall_s (wall time from GNU time).
  * maxrss_kb (peak RSS in KB from GNU time).

Comparison rule (hhh-pa/clojure-code-snippet issue #40): the Bencher
value for Ir is the SUM of per-case MINIMUMS (least-disturbed run) on
CPython exactly as on JVM and clojure-rs, so BMF values compare
directly across runtimes. cpu_time sums per-case medians and
peak_memory takes the max per-case median (bytes) on both sides.
Benchmark names stay stable across the rule change.

GNU time is required (Debian/Ubuntu: apt install time); without it
measure.py fails fast rather than reporting maxrss=0 / wall-clock
cpu approximations. Valgrind remains optional: without it the timed
signals still record but callgrind_instructions stays null.

Usage:
    python3 tools/measure.py --resources tests/resources \
        [--repeat 1] [--callgrind-repeat 1] [--jobs 2] [--timeout 300] \
        [--only substring] [--time-bin BIN] \
        [--output perf.json] [--bmf-output bencher.json] \
        [--summary-file "$GITHUB_STEP_SUMMARY"] [--shard K/N]

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

TOOL_VERSION = 2
_CALLGRIND_TOTAL_RE = re.compile(r"^(?:totals|summary):\s*(\d+)", re.MULTILINE)

# GNU time -f layout; byte-identical to the clojure twin's TimeFormat
# so wall/cpu/RSS fields reconcile field-for-field.
TIME_FORMAT = "wall=%e user=%U sys=%S maxrss_kb=%M cpu_pct=%P major_faults=%F minor_faults=%R"


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


def parse_time_text(text):
    """Parse one GNU time -f TIME_FORMAT line into a metrics dict.

    Mirrors the clojure twin's ParseTimeText: cpu_s is user+sys, and
    any missing/unparseable field is an error, never a silent zero.
    """
    fields = {}
    for token in text.split():
        if "=" in token:
            key, _, value = token.partition("=")
            fields[key] = value
    try:
        wall = float(fields["wall"])
        user = float(fields["user"])
        sys_s = float(fields["sys"])
        maxrss_kb = int(fields["maxrss_kb"])
        cpu_pct = float(fields["cpu_pct"].rstrip("%"))
        major = int(fields["major_faults"])
        minor = int(fields["minor_faults"])
    except (KeyError, ValueError) as exc:
        raise ValueError("unparseable GNU time output: {!r}".format(text.strip())) from exc
    return {
        "wall_s": wall,
        "user_s": user,
        "sys_s": sys_s,
        "cpu_s": user + sys_s,
        "maxrss_kb": maxrss_kb,
        "cpu_pct": cpu_pct,
        "major_faults": major,
        "minor_faults": minor,
    }


def resolve_time_bin(explicit=""):
    """Locate a GNU time binary, mirroring the clojure ResolveTimeBin.

    Raises RuntimeError when none is found (or the candidate is not
    GNU time): the memory signal must be real, never a fallback zero.
    """
    path = explicit
    if not path:
        if os.path.exists("/usr/bin/time"):
            path = "/usr/bin/time"
        else:
            found = shutil.which("time")
            if found:
                path = found
    if not path:
        raise RuntimeError(
            "GNU time not found: install it (Debian/Ubuntu: apt install time) or pass --time-bin"
        )
    try:
        proc = subprocess.run(
            [path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("cannot execute time binary {!r}: {}".format(path, exc)) from exc
    if b"GNU" not in proc.stdout:
        raise RuntimeError(
            "{!r} is not GNU time (need -f/-o support); install GNU time or pass --time-bin".format(
                path
            )
        )
    return path


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


def timed_run_once(time_bin, script, input_path, timeout):
    """One native run under GNU time; returns (stdout, metrics, error)."""
    with open(input_path, "rb") as stdin_fd:
        time_fd, time_file = tempfile.mkstemp(prefix="snip-time-")
        os.close(time_fd)
        try:
            cmd = [time_bin, "-f", TIME_FORMAT, "-o", time_file, sys.executable, script]
            try:
                proc = subprocess.run(
                    cmd,
                    stdin=stdin_fd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                return None, None, "TIMEOUT (>{}s)".format(timeout)
            if proc.returncode != 0:
                err_text = proc.stderr.decode(errors="ignore").strip().splitlines()
                tail = err_text[-1] if err_text else "no stderr"
                return None, None, "exit {}: {}".format(proc.returncode, tail)
            with open(time_file, "r", errors="ignore") as fd:
                raw = fd.read()
        finally:
            try:
                os.unlink(time_file)
            except OSError:
                pass
    try:
        metrics = parse_time_text(raw)
    except ValueError as exc:
        return None, None, "time output unreadable: {}".format(exc)
    return proc.stdout, metrics, None


def callgrind_run_once(script, input_path, timeout):
    """One Valgrind Callgrind run; returns (stdout, ir, error)."""
    fd_temp, callgrind_file = tempfile.mkstemp(prefix="snip-cg-", suffix=".out")
    os.close(fd_temp)
    try:
        cmd = [
            "valgrind",
            "--tool=callgrind",
            "--callgrind-out-file={}".format(callgrind_file),
            sys.executable,
            script,
        ]
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
                return None, None, "TIMEOUT (>{}s)".format(timeout)
        if proc.returncode != 0:
            err_text = proc.stderr.decode(errors="ignore").strip().splitlines()
            tail = err_text[-1] if err_text else "no stderr"
            return None, None, "exit {}: {}".format(proc.returncode, tail)
        instructions = None
        if os.path.isfile(callgrind_file):
            with open(callgrind_file, "r", errors="ignore") as cg_fd:
                instructions = parse_callgrind_output(cg_fd.read())
        return proc.stdout, instructions, None
    finally:
        if os.path.exists(callgrind_file):
            try:
                os.unlink(callgrind_file)
            except OSError:
                pass


def measure_case_callgrind(
    time_bin, has_valgrind, script, case_name, input_path, output_path,
    repeat, callgrind_repeat, timeout,
):
    """Measure one case: GNU-timed native runs plus Callgrind Ir runs.

    A timed-run failure (timeout/crash/mismatch) fails the case, as
    before; callgrind failures fail it too (CPython has no timeout
    budget problem at --timeout 300, so no skip-degradation like the
    JVM twin's slow legs). Returns (summary, error).
    """
    with open(output_path, "rb") as fd:
        expected = run_tests.normalize(fd.read())

    walls, cpus, rss = [], [], []
    for i in range(repeat):
        stdout, metrics, err = timed_run_once(time_bin, script, input_path, timeout)
        if err is not None:
            return None, err
        if i == 0 and run_tests.normalize(stdout) != expected:
            got = run_tests.normalize(stdout).decode(errors="ignore")
            want = expected.decode(errors="ignore")
            return None, "output mismatch: expected {!r} got {!r}".format(want[:100], got[:100])
        walls.append(metrics["wall_s"])
        cpus.append(metrics["cpu_s"])
        rss.append(metrics["maxrss_kb"])

    insn_vals = []
    if has_valgrind:
        for i in range(callgrind_repeat):
            stdout, ir, err = callgrind_run_once(script, input_path, timeout)
            if err is not None:
                return None, err
            if i == 0 and run_tests.normalize(stdout) != expected:
                got = run_tests.normalize(stdout).decode(errors="ignore")
                want = expected.decode(errors="ignore")
                return (
                    None,
                    "callgrind output mismatch: expected {!r} got {!r}".format(
                        want[:100], got[:100]
                    ),
                )
            if ir is not None:
                insn_vals.append(ir)

    summary = {
        "callgrind_instructions": summarize_numbers(insn_vals) if insn_vals else None,
        "wall_s": summarize_numbers(walls),
        "cpu_s": summarize_numbers(cpus),
        "maxrss_kb": summarize_numbers(rss),
        "runs": repeat,
        "callgrind_runs": callgrind_repeat if has_valgrind else 0,
    }
    return summary, None


def build_bmf(results):
    """Aggregate per-snippet summaries into Bencher Metric Format JSON.

    Comparison rule (issue #40): callgrind_instructions is the sum of
    per-case MINIMUMS, cpu_time the sum of per-case medians, and
    peak_memory the max per-case median in bytes -- the same
    aggregations as the clojure twin, so values compare directly.
    """
    snippets = {}
    for r in results:
        label = r["label"]
        snippets.setdefault(label, []).append(r)

    bmf = {}
    for name in sorted(snippets):
        items = snippets[name]
        insn_min, insn_max = [], []
        cpu_min, cpu_med, cpu_max = [], [], []
        rss_min, rss_med, rss_max = [], [], []

        for it in items:
            s = it.get("summary")
            if not s:
                continue
            cg = s.get("callgrind_instructions")
            if cg and cg.get("min") is not None:
                insn_min.append(cg["min"])
                insn_max.append(cg["max"])
            cpu = s.get("cpu_s")
            if cpu and cpu.get("median") is not None:
                cpu_min.append(cpu["min"])
                cpu_med.append(cpu["median"])
                cpu_max.append(cpu["max"])
            rss = s.get("maxrss_kb")
            if rss and rss.get("median") is not None:
                rss_min.append(rss["min"])
                rss_med.append(rss["median"])
                rss_max.append(rss["max"])

        measures = {}
        if insn_min:
            lo = int(sum(insn_min))
            measures["callgrind_instructions"] = {
                "value": lo,
                "lower_value": lo,
                "upper_value": int(sum(insn_max)),
            }
        if cpu_med:
            measures["cpu_time"] = {
                "value": float(sum(cpu_med)),
                "lower_value": float(sum(cpu_min)),
                "upper_value": float(sum(cpu_max)),
            }
        if rss_med:
            measures["peak_memory"] = {
                "value": max(rss_med) * 1024,
                "lower_value": max(rss_min) * 1024,
                "upper_value": max(rss_max) * 1024,
            }

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
        "### Callgrind Performance Summary (Python)",
        "",
        "| Benchmark | Cases | Instructions (Ir) | CPU Time (s) | Peak RSS (MB) |",
        "| :--- | :---: | :---: | :---: | :---: |",
    ]

    total_insn = 0
    total_cpu = 0.0
    peak_rss = 0
    has_insn = False

    snippets = {}
    for r in report.get("results", []):
        snippets.setdefault(r["label"], []).append(r)

    for name in sorted(snippets):
        cases_count = len(snippets[name])
        m = bmf.get(name, {})
        insn_str = "-"
        if "callgrind_instructions" in m:
            val = m["callgrind_instructions"]["value"]
            insn_str = "{:,}".format(val)
            total_insn += val
            has_insn = True
        cpu_val = m.get("cpu_time", {}).get("value", 0.0)
        total_cpu += cpu_val
        rss_mb = m.get("peak_memory", {}).get("value", 0) / (1024 * 1024)
        peak_rss = max(peak_rss, m.get("peak_memory", {}).get("value", 0))
        lines.append(
            "| `{}` | {} | {} | {:.4f} | {:.1f} |".format(name, cases_count, insn_str, cpu_val, rss_mb)
        )

    tot_insn_str = "{:,}".format(total_insn) if has_insn else "-"
    lines.append(
        "| **Total ({} snippets)** | - | **{}** | **{:.4f}** | **{:.1f}** |".format(
            len(snippets), tot_insn_str, total_cpu, peak_rss / (1024 * 1024)
        )
    )
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
    assert parsed == 987654321, "Expected 987654321, got {}".format(parsed)

    sample_time = "wall=1.23 user=0.90 sys=0.10 maxrss_kb=123456 cpu_pct=81% major_faults=2 minor_faults=300\n"
    tm = parse_time_text(sample_time)
    assert tm["wall_s"] == 1.23, tm
    assert tm["cpu_s"] == 1.0, tm
    assert tm["maxrss_kb"] == 123456, tm
    assert tm["cpu_pct"] == 81.0, tm
    for bad in ["garbage line\n", "wall=1.0 user=0.5\n"]:
        try:
            parse_time_text(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("parse_time_text accepted {!r}".format(bad))

    # resolve_time_bin against hermetic fake `time` binaries.
    fake_dir = tempfile.mkdtemp(prefix="snip-time-test-")
    try:
        gnu = os.path.join(fake_dir, "gnu-time")
        with open(gnu, "w") as fd:
            fd.write("#!/bin/sh\necho 'GNU time 1.9'\n")
        os.chmod(gnu, 0o755)
        assert resolve_time_bin(gnu) == gnu
        bsd = os.path.join(fake_dir, "bsd-time")
        with open(bsd, "w") as fd:
            fd.write("#!/bin/sh\necho 'usage: time' >&2\nexit 1\n")
        os.chmod(bsd, 0o755)
        try:
            resolve_time_bin(bsd)
        except RuntimeError:
            pass
        else:
            raise AssertionError("resolve_time_bin accepted non-GNU time")
        try:
            resolve_time_bin(os.path.join(fake_dir, "missing"))
        except RuntimeError:
            pass
        else:
            raise AssertionError("resolve_time_bin accepted a missing binary")
    finally:
        shutil.rmtree(fake_dir, ignore_errors=True)

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

    # BMF: Ir sums per-case MINs (comparison rule), cpu sums
    # medians, peak takes the max median in bytes -- all with
    # lower/upper bounds mirroring the clojure twin.
    mock_results = [
        {
            "label": "sort/merge_sort",
            "case": "tc0",
            "summary": {
                "callgrind_instructions": {"min": 900, "median": 1000, "max": 1100},
                "cpu_s": {"min": 0.04, "median": 0.05, "max": 0.06},
                "maxrss_kb": {"min": 90, "median": 100, "max": 110},
            },
        },
        {
            "label": "sort/merge_sort",
            "case": "tc1",
            "summary": {
                "callgrind_instructions": {"min": 1900, "median": 2000, "max": 2100},
                "cpu_s": {"min": 0.06, "median": 0.07, "max": 0.08},
                "maxrss_kb": {"min": 190, "median": 200, "max": 210},
            },
        },
        {
            "label": "sort/quick_sort",
            "case": "tc0",
            "summary": {
                "callgrind_instructions": None,
                "cpu_s": {"min": 0.01, "median": 0.02, "max": 0.03},
                "maxrss_kb": {"min": 50, "median": 60, "max": 70},
            },
        },
    ]
    bmf = build_bmf(mock_results)
    merge_entry = bmf["sort/merge_sort"]
    assert merge_entry["callgrind_instructions"]["value"] == 2800, merge_entry
    assert merge_entry["callgrind_instructions"]["lower_value"] == 2800, merge_entry
    assert merge_entry["callgrind_instructions"]["upper_value"] == 3200, merge_entry
    assert abs(merge_entry["cpu_time"]["value"] - 0.12) < 1e-9, merge_entry
    assert merge_entry["peak_memory"]["value"] == 200 * 1024, merge_entry
    assert merge_entry["peak_memory"]["lower_value"] == 190 * 1024, merge_entry
    assert merge_entry["peak_memory"]["upper_value"] == 210 * 1024, merge_entry
    # No Ir anywhere: the measure stays absent (like the twin).
    assert "callgrind_instructions" not in bmf["sort/quick_sort"], bmf["sort/quick_sort"]
    assert "cpu_time" in bmf["sort/quick_sort"]

    # Merge fan-in: dedupe by (label, case), union BMF keys.
    rep_a = {
        "results": [mock_results[0], mock_results[2]],
        "failures": ["x: boom"],
    }
    rep_b = {
        "results": [mock_results[0], mock_results[1]],
        "failures": [],
    }
    merge_dir = tempfile.mkdtemp(prefix="snip-merge-test-")
    try:
        pa = os.path.join(merge_dir, "a.json")
        pb = os.path.join(merge_dir, "b.json")
        with open(pa, "w") as fd:
            json.dump(rep_a, fd)
        with open(pb, "w") as fd:
            json.dump(rep_b, fd)
        merged, merged_bmf = merge_reports([pa, pb])
        assert len(merged["results"]) == 3, merged
        assert merged["failures"] == ["x: boom"], merged
        assert (
            merged_bmf["sort/merge_sort"]["callgrind_instructions"]["value"] == 2800
        ), merged_bmf
    finally:
        shutil.rmtree(merge_dir, ignore_errors=True)

    print("self-test passed!")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default=os.path.join(ROOT, "tests", "resources"))
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument(
        "--callgrind-repeat", type=int, default=1,
        help="Valgrind Callgrind runs per case for Ir (timed runs use --repeat)",
    )
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--only", default="", help="filter by label substring")
    parser.add_argument("--time-bin", default="", help="GNU time binary (default: auto-detect)")
    parser.add_argument("--shard", default="", help="shard K/N (0-based K)")
    parser.add_argument("--output", default=None, help="JSON output file")
    parser.add_argument("--bmf-output", default=None, help="Bencher Metric Format output")
    parser.add_argument("--summary-file", default=None, help="Markdown summary output")
    parser.add_argument("--merge", nargs="*", default=None, help="merge shard JSON files")
    parser.add_argument("--self-test", action="store_true", help="run self-test")
    args = parser.parse_args(argv)

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
        print(
            "Merged {} reports: {} cases, {} benchmarks.".format(
                len(args.merge), len(report["results"]), len(bmf)
            )
        )
        return 0

    if args.repeat < 1:
        print("measure.py: --repeat must be >= 1", file=sys.stderr)
        return 2
    if args.callgrind_repeat < 1:
        print("measure.py: --callgrind-repeat must be >= 1", file=sys.stderr)
        return 2

    try:
        time_bin = resolve_time_bin(args.time_bin)
    except RuntimeError as exc:
        print("measure.py: {}".format(exc), file=sys.stderr)
        return 1

    has_valgrind = shutil.which("valgrind") is not None
    if not has_valgrind:
        print(
            "warning: valgrind not found in PATH; recording timed signals without Callgrind Ir",
            file=sys.stderr,
        )

    tasks = []
    missing = []
    for area, problem, stem, script, cases in run_tests.discover(args.resources):
        label = "{}/{}/{}".format(area, problem, stem) if problem != stem else "{}/{}".format(
            area, problem
        )
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
    print(
        "Measuring {} cases ({} benchmarks) with GNU time{}...".format(
            total_tasks,
            len({t[0] for t in tasks}),
            " + Callgrind" if has_valgrind else "",
        )
    )

    results = []
    failures = []
    done = 0

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                measure_case_callgrind,
                time_bin,
                has_valgrind,
                script,
                case_name,
                inp,
                outp,
                args.repeat,
                args.callgrind_repeat,
                args.timeout,
            ): (label, stem, script, case_name)
            for label, stem, script, case_name, inp, outp in tasks
        }
        for future in as_completed(futures):
            label, stem, script, case_name = futures[future]
            summary, err = future.result()
            done += 1
            if err is None:
                cg = summary.get("callgrind_instructions")
                insn_s = "{:,} Ir".format(int(cg["min"])) if cg else "n/a"
                print("[{}/{}] {}/{}: {}".format(done, total_tasks, label, case_name, insn_s))
                results.append(
                    {
                        "label": label,
                        "stem": stem,
                        "case": case_name,
                        "script": os.path.relpath(script, ROOT),
                        "summary": summary,
                    }
                )
            else:
                print("[{}/{}] FAIL {}/{}: {}".format(done, total_tasks, label, case_name, err))
                failures.append("{}/{}: {}".format(label, case_name, err))

    report = {
        "tool_version": TOOL_VERSION,
        "platform": platform.platform(),
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "has_valgrind": has_valgrind,
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
