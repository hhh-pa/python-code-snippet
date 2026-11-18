"""Weighted fair queueing (Tanenbaum 5.4 finish-tag formula)."""

import math
import sys


def _run(weights, packets):
    f = len(weights)
    den = 1
    for w in weights:
        den = den * w // math.gcd(den, w)
    last = [0] * f
    tags = []
    for flow, arr, ln in packets:
        tag = max(arr * den, last[flow]) + ln * (den // weights[flow])
        last[flow] = tag
        tags.append(tag)
    order = []
    done = [False] * len(packets)
    now = 0
    while len(order) < len(packets):
        best = -1
        for i, (flow, arr, _) in enumerate(packets):
            if done[i] or arr > now:
                continue
            if best < 0 or (tags[i], arr, flow, i) < (
                tags[best],
                packets[best][1],
                packets[best][0],
                best,
            ):
                best = i
        if best < 0:
            now = min(p[1] for i, p in enumerate(packets) if not done[i])
            continue
        done[best] = True
        order.append(best)
        now += packets[best][2]
    fracs = []
    for i in order:
        g = math.gcd(tags[i], den)
        fracs.append(f"{tags[i] // g}/{den // g}")
    return " ".join(map(str, order)) + "\n" + " ".join(fracs)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    f, m = int(toks[0]), int(toks[1])
    weights = list(map(int, toks[2 : 2 + f]))
    packets = []
    i = 2 + f
    for _ in range(m):
        packets.append((int(toks[i]), int(toks[i + 1]), int(toks[i + 2])))
        i += 3
    sys.stdout.write(_run(weights, packets))


if __name__ == "__main__":
    main()
