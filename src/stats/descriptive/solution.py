"""Descriptive statistics + Cohen's d (Think Stats 2e ch 1-2)."""

import math
import sys


def _stats(xs):
    n = len(xs)
    mean = sum(xs) / n
    var = sum((x - mean) * (x - mean) for x in xs) / (n - 1)
    srt = sorted(xs)
    med = float(srt[n // 2]) if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    return n, mean, var, math.sqrt(var), min(xs), max(xs), med


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n1 = int(toks[0])
    g1 = list(map(int, toks[1 : 1 + n1]))
    n2 = int(toks[1 + n1])
    g2 = list(map(int, toks[2 + n1 : 2 + n1 + n2]))
    _, m1, v1, s1, mn1, mx1, md1 = _stats(g1)
    _, m2, v2, s2, mn2, mx2, md2 = _stats(g2)
    t1 = n1 * v1
    t2 = n2 * v2
    pv = (t1 + t2) / (n1 + n2)
    d = (m1 - m2) / math.sqrt(pv)
    out = [
        f"{n1} {m1:.6f} {v1:.6f} {s1:.6f} {mn1} {mx1} {md1:.6f}",
        f"{n2} {m2:.6f} {v2:.6f} {s2:.6f} {mn2} {mx2} {md2:.6f}",
        f"COHEN {d:.6f}",
    ]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
