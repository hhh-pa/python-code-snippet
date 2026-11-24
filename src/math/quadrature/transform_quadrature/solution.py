# Quadrature by variable transformation (NR 4.5).
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    fun = toks[1]
    if fun == "POLY":
        d = int(toks[2])
        p = [float(v) for v in toks[3:4 + d]]
        rest = 4 + d
    elif fun == "POW":
        p = [float(v) for v in toks[2:6]]
        rest = 6
    else:
        p = [float(v) for v in toks[2:5]]
        rest = 5

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

    def tx(rule, t):
        if rule == "SEMIINF_DE":
            x = math.exp(math.pi * math.sinh(t))
            return x, x * math.pi * math.cosh(t)
        if rule == "SEMIINF_TANH":
            x = math.exp(t)
            return x, x
        if rule == "INF_TANH":
            return math.sinh(t), math.cosh(t)
        x = math.exp(t - math.exp(-t))
        return x, x * (1.0 + math.exp(-t))

    def traprange(rule, lo, hi, l, sgn):
        def g(t):
            x, dxdt = tx(rule, t)
            return f(sgn * x) * dxdt

        n = 0
        s = 0.0
        for _ in range(l):
            n += 1
            if n == 1:
                s = 0.5 * (hi - lo) * (g(lo) + g(hi))
            else:
                it = 1
                for _ in range(1, n - 1):
                    it <<= 1
                tnm = float(it)
                dl = (hi - lo) / tnm
                x = lo + 0.5 * dl
                sm = 0.0
                for _ in range(it):
                    sm += g(x)
                    x += dl
                s = 0.5 * (s + (hi - lo) * sm / tnm)
        return s

    if op == "DE_FINITE":
        a = float(toks[rest])
        b = float(toks[rest + 1])
        hmax = float(toks[rest + 2])
        l = int(toks[rest + 3])
        s = 0.0
        for n in range(1, l + 1):
            if n == 1:
                s = hmax * 2.0 * (b - a) * 0.25 * f(0.5 * (b + a))
            else:
                it = 1
                for _ in range(1, n - 1):
                    it <<= 1
                twoh = hmax / it
                t = 0.5 * twoh
                sm = 0.0
                for _ in range(it):
                    q = math.exp(-2.0 * math.sinh(t))
                    dl = (b - a) * q / (1.0 + q)
                    fact = q / ((1.0 + q) * (1.0 + q)) * math.cosh(t)
                    sm += fact * (f(a + dl) + f(b - dl))
                    t += twoh
                s = 0.5 * s + (b - a) * twoh * sm
        ans = s
    else:
        t0 = float(toks[rest])
        t1 = float(toks[rest + 1])
        l = int(toks[rest + 2])
        if op == "INF_MIXED":
            ans = traprange("SEMIINF_MIXED", t0, t1, l, 1.0) + traprange(
                "SEMIINF_MIXED", t0, t1, l, -1.0)
        else:
            ans = traprange(op, t0, t1, l, 1.0)
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
