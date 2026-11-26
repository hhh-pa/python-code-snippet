"""Breeden-Litzenberger density + CDF (FE ch 15)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    t = float(toks[0])
    r = float(toks[1])
    m = int(toks[2])
    ks = [0.0] * m
    calls = [0.0] * m
    for i in range(m):
        ks[i] = float(toks[3 + 2 * i])
        calls[i] = float(toks[4 + 2 * i])
    h = ks[1] - ks[0]
    disc = math.exp(r * t)
    out = []
    for i in range(1, m - 1):
        d2 = (calls[i + 1] - (2 * calls[i]) + calls[i - 1]) / (h * h)
        f = disc * d2
        d1 = (calls[i + 1] - calls[i - 1]) / (2 * h)
        cdf = 1 + disc * d1
        out.append(f"{ks[i]:.6f} {f:.6f} {cdf:.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
