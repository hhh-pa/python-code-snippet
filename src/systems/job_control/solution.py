"""Shell job control (CS:APP ch 8 + Shell Lab)."""

import sys


def _fg(jobs):
    for jid in sorted(jobs):
        if jobs[jid][1] == "FG":
            return jid
    return None


def _ev_run(jobs, nextjid, pid, cmd, bg):
    if bg == 0 and _fg(jobs) is not None:
        return ["REJECTED"], nextjid
    jobs[nextjid] = [pid, "FG" if bg == 0 else "BG", cmd]
    return [f"JOB {nextjid} {pid}"], nextjid + 1


def _ev_sig(jobs, op):
    f = _fg(jobs)
    if f is None:
        return ["NOJOB"]
    if op == "INT":
        del jobs[f]
        return [f"TERM {f}"]
    jobs[f][1] = "ST"
    return [f"STOP {f}"]


def _ev_fg(jobs, jid):
    if jid not in jobs:
        return ["NOJOB"]
    if _fg(jobs) is not None and _fg(jobs) != jid:
        return ["REJECTED"]
    jobs[jid][1] = "FG"
    return [f"FG {jid}"]


def _ev_bg(jobs, jid):
    if jid not in jobs:
        return ["NOJOB"]
    if jobs[jid][1] == "FG":
        return ["REJECTED"]
    jobs[jid][1] = "BG"
    return [f"BG {jid}"]


def _ev_kill(jobs, jid):
    if jid not in jobs:
        return ["NOJOB"]
    del jobs[jid]
    return [f"TERM {jid}"]


def _ev_exit(jobs, pid):
    for jid in sorted(jobs):
        if jobs[jid][0] == pid:
            del jobs[jid]
            return [f"DONE {jid}"]
    return ["NOJOB"]


def _ev_jobs(jobs):
    if not jobs:
        return ["NOJOBS"]
    return [
        f"{jid} {jobs[jid][0]} {jobs[jid][1]} {jobs[jid][2]}" for jid in sorted(jobs)
    ]


def _run(events):
    jobs = {}
    nextjid = 1
    out = []
    for ev in events:
        if ev[0] == "RUN":
            lines, nextjid = _ev_run(jobs, nextjid, *ev[1:])
        elif ev[0] in ("INT", "TSTP"):
            lines = _ev_sig(jobs, ev[0])
        elif ev[0] == "FG":
            lines = _ev_fg(jobs, ev[1])
        elif ev[0] == "BG":
            lines = _ev_bg(jobs, ev[1])
        elif ev[0] == "KILL":
            lines = _ev_kill(jobs, ev[1])
        elif ev[0] == "EXIT":
            lines = _ev_exit(jobs, ev[1])
        else:
            lines = _ev_jobs(jobs)
        out += lines
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    e = int(toks[0])
    events = []
    i = 1
    for _ in range(e):
        op = toks[i]
        if op == "RUN":
            events.append(("RUN", int(toks[i + 1]), toks[i + 2], int(toks[i + 3])))
            i += 4
        elif op in ("FG", "BG", "KILL", "EXIT"):
            events.append((op, int(toks[i + 1])))
            i += 2
        else:
            events.append((op,))
            i += 1
    sys.stdout.write("\n".join(_run(events)))


if __name__ == "__main__":
    main()
