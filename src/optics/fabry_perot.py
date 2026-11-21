"""Fabry-Perot etalon transmission (wave ch 3)."""

import math
import sys


def _snap(x):
    return 0.0 if abs(x) < 5e-7 else x


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    r = float(toks[0])
    n = float(toks[1])
    d = float(toks[2])
    theta = float(toks[3])
    m = int(toks[4])
    lams = list(map(float, toks[5 : 5 + m]))
    fcoef = 4 * r / ((1 - r) * (1 - r))
    finesse = math.pi * math.sqrt(r) / (1 - r)
    trad = theta * math.pi / 180
    cost = math.cos(trad)
    out = [f"FINESSE {_snap(finesse):.6f}"]
    for lam in lams:
        k = (4 * math.pi) / lam
        de = k * n * d * cost
        s = math.sin(de / 2)
        t = 1 / (1 + fcoef * s * s)
        out.append(f"T {_snap(t):.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
