#!/usr/bin/env python3
"""Self-contained correctness runner for the Python snippet repo.

For every solution script under src/<area>/<problem>/<file>.py this runs
`python3 <file>.py` once per shared test case and diff-compares stdout
against the expected output (trailing whitespace per line ignored,
same as the recipes superproject harness).

Resources live OUTSIDE this repo (they belong to the recipes superproject).
Layout expected under --resources DIR:

    DIR/<area>/<problem>/<file-stem>/test_case_N/input.txt
    DIR/<area>/<problem>/<file-stem>/test_case_N/output.txt

Usage:
    python3 tests/run_tests.py --resources tests/resources \
        [--jobs N] [--timeout 120] [--only substring] [--shard I/N]

Shard I/N runs only the deterministic slice of the sorted task list
(task index mod N == I-1), so CI can split the suite across jobs.

Exit status is non-zero when any case fails or a case is missing resources.
"""

import argparse
import glob
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def normalize(content):
    return b"\n".join(line.strip() for line in content.splitlines())


def discover(resources_root):
    """Yield (area, problem, stem, script_path, [(case_name, in, out), ...])."""
    for script in sorted(glob.glob(os.path.join(ROOT, "src", "**", "*.py"), recursive=True)):
        rel = os.path.relpath(script, os.path.join(ROOT, "src"))
        rel_stem = os.path.splitext(rel)[0]
        case_dir = os.path.join(resources_root, rel_stem)
        cases = []
        for case in sorted(glob.glob(os.path.join(case_dir, "test_case_*"))):
            if os.path.isdir(case):
                cases.append(
                    (
                        os.path.basename(case),
                        os.path.join(case, "input.txt"),
                        os.path.join(case, "output.txt"),
                    )
                )
        parts = rel_stem.split(os.sep)
        if len(parts) >= 2:
            area = parts[0]
            problem = "/".join(parts[1:-1]) if len(parts) > 2 else parts[1]
            stem = parts[-1]
        else:
            area, problem, stem = parts[0], parts[0], parts[0]
        yield area, problem, stem, script, cases


def run_case(script, case_name, input_path, output_path, timeout):
    with open(input_path, "rb") as fd:
        try:
            proc = subprocess.run(
                [sys.executable, script],
                stdin=fd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return "TIMEOUT (>{}s)".format(timeout)
    if proc.returncode != 0:
        tail = proc.stderr.decode(errors="ignore").strip().splitlines()
        return "exit {}: {}".format(proc.returncode, tail[-1] if tail else "no stderr")
    with open(output_path, "rb") as fd:
        expected = normalize(fd.read())
    if normalize(proc.stdout) != expected:
        got = normalize(proc.stdout).decode(errors="ignore")
        want = expected.decode(errors="ignore")
        return "output mismatch: expected {!r} got {!r}".format(want[:200], got[:200])
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resources", default=os.path.join(ROOT, "tests", "resources"))
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--only", default="", help="substring filter on area/problem")
    parser.add_argument("--shard", default="", help="shard slice I/N (1-based I)")
    args = parser.parse_args(argv)
    shard_index, shard_total = 0, 1
    if args.shard:
        try:
            picked, total = args.shard.split("/")
            shard_index, shard_total = int(picked) - 1, int(total)
        except ValueError:
            raise SystemExit("bad --shard {!r}: want I/N".format(args.shard))
        if not 0 <= shard_index < shard_total:
            raise SystemExit("bad --shard {!r}: want 1 <= I <= N".format(args.shard))

    tasks = []
    missing = []
    for area, problem, stem, script, cases in discover(args.resources):
        label = f"{area}/{problem}/{stem}" if problem != stem else f"{area}/{problem}"
        if args.only and args.only not in label and args.only not in script:
            continue
        if not cases:
            missing.append(label)
            continue
        for case_name, inp, outp in cases:
            tasks.append((label, case_name, script, inp, outp))

    tasks = sorted(tasks)
    if shard_total > 1:
        tasks = [task for index, task in enumerate(tasks) if index % shard_total == shard_index]
    total = len(tasks)
    print("python tests: {} cases{} ({} problems)".format(
        total,
        " [shard {}/{}]".format(shard_index + 1, shard_total) if shard_total > 1 else "",
        len({label for label, _, _, _, _ in tasks}),
    ), flush=True)

    failures = []
    passed = 0
    done = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(run_case, script, case, inp, outp, args.timeout): (label, case)
            for label, case, script, inp, outp in tasks
        }
        for future in as_completed(futures):
            label, case = futures[future]
            error = future.result()
            done += 1
            if error is None:
                passed += 1
                print("PASS {}/{} [{}/{}]".format(label, case, done, total), flush=True)
            else:
                failures.append("{}/{}: {}".format(label, case, error))
                print("FAIL {}/{} [{}/{}]: {}".format(label, case, done, total, error), flush=True)

    for label in missing:
        failures.append("{}: no resources found".format(label))
    for failure in sorted(failures):
        print("FAIL", failure)
    print(
        "python tests: {} passed, {} failed, {} missing-resource problems".format(
            passed, len(failures) - len(missing), len(missing)
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
