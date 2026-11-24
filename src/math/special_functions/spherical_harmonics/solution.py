# Spherical harmonics (NR 6.7).
import math
import sys


def plegendre(l, m, x):
    pmm = 1.0
    if m > 0:
        omx2 = (1.0 - x) * (1.0 + x)
        fact = 1.0
        for _ in range(1, m + 1):
            pmm *= omx2 * fact / (fact + 1.0)
            fact += 2.0
    pmm = math.sqrt((2 * m + 1) * pmm / (4.0 * math.pi))
    if m & 1:
        pmm = -pmm
    if l == m:
        return pmm
    pmmp1 = x * math.sqrt(2.0 * m + 3.0) * pmm
    if l == m + 1:
        return pmmp1
    oldfact = math.sqrt(2.0 * m + 3.0)
    pll = 0.0
    for ll in range(m + 2, l + 1):
        fact = math.sqrt((4.0 * ll * ll - 1.0) / (ll * ll - m * m))
        pll = (x * pmmp1 - pmm / oldfact) * fact
        oldfact = fact
        pmm = pmmp1
        pmmp1 = pll
    return pll


def plgndr(l, m, x):
    prod = 1.0
    for j in range(l - m + 1, l + m + 1):
        prod *= j
    return math.sqrt(4.0 * math.pi * prod / (2 * l + 1)) * plegendre(l, m, x)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op in ("PLEG", "PLM"):
        l = int(toks[1])
        m = int(toks[2])
        x = float(toks[3])
        ans = plegendre(l, m, x) if op == "PLEG" else plgndr(l, m, x)
        w = 0.0 if abs(ans) < 5e-7 else ans
        sys.stdout.write("%.6f\n" % (w + 0.0))
    else:
        l = int(toks[1])
        m = int(toks[2])
        th = float(toks[3])
        ph = float(toks[4])
        if m >= 0:
            pt = plegendre(l, m, math.cos(th))
            re = pt * math.cos(m * ph)
            im = pt * math.sin(m * ph)
        else:
            pt = plegendre(l, -m, math.cos(th))
            s = -1.0 if (-m) & 1 else 1.0
            re = s * pt * math.cos(m * ph)
            im = s * pt * math.sin(m * ph)
        re = 0.0 if abs(re) < 5e-7 else re
        im = 0.0 if abs(im) < 5e-7 else im
        sys.stdout.write("%.6f %.6f\n" % (re + 0.0, im + 0.0))


main()
