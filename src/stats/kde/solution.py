"""Gaussian kernel density estimation (Think Stats 2e ch 6)."""

import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    xs = list(map(float, toks[1 : 1 + n]))
    h = float(toks[1 + n])
    m = int(toks[2 + n])
    qs = list(map(float, toks[3 + n : 3 + n + m]))
    coef = 1 / (h * math.sqrt(2 * math.pi))
    denom = (2 * h) * h
    out = []
    for q in qs:
        s = 0.0
        for x in xs:
            d = q - x
            s += math.exp(-((d * d) / denom))
        out.append(f"{(coef * s) / n:.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
