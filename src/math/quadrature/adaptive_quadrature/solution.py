# Adaptive quadrature (NR 4.7).
import math
import sys

sys.setrecursionlimit(10000)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    fun = toks[0]
    if fun == "POLY":
        d = int(toks[1])
        p = [float(v) for v in toks[2:3 + d]]
        rest = 3 + d
    elif fun == "POW":
        p = [float(v) for v in toks[1:5]]
        rest = 5
    else:
        p = [float(v) for v in toks[1:4]]
        rest = 4
    a = float(toks[rest])
    b = float(toks[rest + 1])
    eps = float(toks[rest + 2])

    def f(t):
        if fun == "POLY":
            s = 0.0
            for c in reversed(p):
                s = s * t + c
            return s
        if fun == "EXP":
            return p[0] * math.exp(p[1] * t) + p[2]
        if fun == "TRIG":
            return p[0] * math.sin(p[1] * t + p[2])
        if fun == "LOG":
            return p[0] * math.log(p[1] * t + p[2])
        if fun == "GAUSS":
            z = (t - p[1]) / p[2]
            return p[0] * math.exp(-z * z)
        return p[0] * math.pow(p[1] * t + p[2], p[3])

    r5 = 1.0 / math.sqrt(5.0)
    r23 = math.sqrt(2.0 / 3.0)

    def lobatto4(aa, bb):
        m = 0.5 * (aa + bb)
        h = 0.5 * (bb - aa)
        return h * ((f(m - h) + f(m + h)) / 6.0 +
                    5.0 * (f(m - h * r5) + f(m + h * r5)) / 6.0)

    def kronrod7(aa, bb):
        m = 0.5 * (aa + bb)
        h = 0.5 * (bb - aa)
        return h * (11.0 * (f(m - h) + f(m + h)) / 210.0 +
                    72.0 * (f(m - h * r23) + f(m + h * r23)) / 245.0 +
                    125.0 * (f(m - h * r5) + f(m + h * r5)) / 294.0 +
                    16.0 * f(m) / 35.0)

    iscale = kronrod7(a, b)
    oot = False

    def rec(aa, bb, depth):
        nonlocal oot
        i1 = kronrod7(aa, bb)
        i2 = lobatto4(aa, bb)
        m = 0.5 * (aa + bb)
        if abs(i1 - i2) <= eps * abs(iscale):
            return i1
        if depth >= 12 or m <= aa or bb <= m:
            oot = True
            return i1
        return rec(aa, m, depth + 1) + rec(m, bb, depth + 1)

    ans = rec(a, b, 0)
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f %d\n" % (w + 0.0, 1 if oot else 0))


main()
