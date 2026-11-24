# Dawson's integral (NR 6.9).
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    x = float(toks[0])
    nmax = 6
    hstep = 0.4
    a1 = 2.0 / 3.0
    a2 = 0.4
    a3 = 2.0 / 7.0
    ct = [(2.0 * i + 1.0) * hstep for i in range(nmax)]
    c = [math.exp(-(t * t)) for t in ct]
    if abs(x) < 0.2:
        x2 = x * x
        ans = x * (1.0 - a1 * x2 * (1.0 - a2 * x2 * (1.0 - a3 * x2)))
    else:
        xx = abs(x)
        n0 = 2 * int(0.5 * xx / hstep + 0.5)
        xp = xx - n0 * hstep
        e1 = math.exp(2.0 * xp * hstep)
        e2 = e1 * e1
        d1 = n0 + 1.0
        d2 = d1 - 2.0
        sm = 0.0
        for i in range(nmax):
            sm += c[i] * (e1 / d1 + 1.0 / (d2 * e1))
            d1 += 2.0
            d2 -= 2.0
            e1 *= e2
        s = math.exp(-xp * xp)
        if x < 0.0:
            s = -s
        ans = 0.5641895835 * s * sm
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
