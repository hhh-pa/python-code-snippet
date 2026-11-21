"""PMF/CDF queries (Think Stats 2e ch 3-4)."""

import math
import sys


def _half_even(x):
    q = math.floor(x)
    f = x - q
    if f > 0.5:
        return q + 1
    if f < 0.5:
        return q
    return q if q % 2 == 0 else q + 1


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    xs = list(map(int, toks[1 : 1 + n]))
    srt = sorted(xs)
    i = 1 + n
    q = int(toks[i])
    i += 1
    out = []
    for _ in range(q):
        op = toks[i]
        if op == "PCTL":
            p = float(toks[i + 1])
            i += 2
            r = (p * (n + 1)) / 100
            rank = min(n, max(1, _half_even(r)))
            out.append(str(srt[rank - 1]))
        else:
            v = int(toks[i + 1])
            i += 2
            if op == "PMF":
                out.append(f"{sum(1 for x in xs if x == v) / n:.6f}")
            elif op == "CDF":
                out.append(f"{sum(1 for x in xs if x <= v) / n:.6f}")
            else:
                out.append(f"{(100 * sum(1 for x in xs if x <= v)) / n:.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
