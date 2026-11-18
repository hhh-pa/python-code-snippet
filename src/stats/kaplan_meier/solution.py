"""Kaplan-Meier survival analysis (Think Stats 2e ch 13)."""

import sys


def _km_curve(times, events):
    taus = sorted({t for t, e in zip(times, events) if e == 1})
    survs = []
    hazards = []
    s = 1.0
    for tau in taus:
        d = sum(1 for t, e in zip(times, events) if t == tau and e == 1)
        nr = sum(1 for t in times if t >= tau)
        s *= (nr - d) / nr
        survs.append(s)
        hazards.append(d / nr)
    return taus, survs, hazards


def _remaining(taus, survs, query):
    if not taus or query >= taus[-1]:
        return 0.0
    sq = 1.0
    for tau, ss in zip(taus, survs):
        if tau <= query:
            sq = ss
        else:
            break
    if sq == 0.0:
        return 0.0
    area = 0.0
    prev_t = 0
    prev_s = 1.0
    for idx, tau in enumerate(taus):
        if tau > query:
            lo = prev_t if prev_t > query else query
            area += prev_s * (tau - lo)
        prev_t = tau
        prev_s = survs[idx]
    return area / sq


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    times = [0] * n
    events = [0] * n
    for i in range(n):
        times[i] = int(toks[1 + 2 * i])
        events[i] = int(toks[2 + 2 * i])
    q = int(toks[1 + 2 * n])
    queries = list(map(int, toks[2 + 2 * n : 2 + 2 * n + q]))
    taus, survs, hazards = _km_curve(times, events)
    out = []
    for tau, s, h in zip(taus, survs, hazards):
        out.append(f"SURV {tau} {s:.6f} {h:.6f}")
    for query in queries:
        out.append(f"REM {query} {_remaining(taus, survs, query):.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
