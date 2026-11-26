# Chebyshev approximation (NR 5.8-5.11).
import math
import sys


def fmtv(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def chebev(x, c):
    m = len(c)
    d = 0.0
    dd = 0.0
    for j in range(m - 1, 0, -1):
        sv = d
        d = 2.0 * x * d - dd + c[j]
        dd = sv
    return x * d - dd + 0.5 * c[0]


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "FIT":
        fun = toks[1]
        if fun == "POLY":
            d = int(toks[2])
            p = [float(v) for v in toks[3:4 + d]]
            rest = 4 + d
        else:
            p = [float(v) for v in toks[2:5]]
            rest = 5
        a = float(toks[rest])
        b = float(toks[rest + 1])
        n = int(toks[rest + 2])

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
            return p[0] * math.log(p[1] * t + p[2])

        c = []
        for j in range(n):
            s = 0.0
            for k in range(n):
                y = math.cos(math.pi * (k + 0.5) / n)
                t = 0.5 * ((b - a) * y + (a + b))
                s += f(t) * math.cos(math.pi * j * (k + 0.5) / n)
            c.append(2.0 * s / n)
        sys.stdout.write(" ".join(fmtv(v) for v in c) + "\n")
    elif op == "EVAL":
        n = int(toks[1])
        x = float(toks[2])
        c = [float(v) for v in toks[3:3 + n]]
        sys.stdout.write(fmtv(chebev(x, c)) + "\n")
    elif op == "DERIV":
        n = int(toks[1])
        a = float(toks[2])
        b = float(toks[3])
        c = [float(v) for v in toks[4:4 + n]]
        cd = [0.0] * n
        cd[n - 1] = 0.0
        if n >= 2:
            cd[n - 2] = 2 * (n - 1) * c[n - 1]
        for j in range(n - 2, 0, -1):
            cd[j - 1] = cd[j + 1] + 2 * j * c[j]
        con = 2.0 / (b - a)
        sys.stdout.write(" ".join(fmtv(v * con) for v in cd) + "\n")
    elif op == "INTEG":
        n = int(toks[1])
        a = float(toks[2])
        b = float(toks[3])
        c = [float(v) for v in toks[4:4 + n]]
        ci = [0.0] * n
        con = 0.25 * (b - a)
        s = 0.0
        fac = 1.0
        for j in range(1, n - 1):
            ci[j] = con * (c[j - 1] - c[j + 1]) / j
            s += fac * ci[j]
            fac = -fac
        ci[n - 1] = con * c[n - 2] / (n - 1)
        s += fac * ci[n - 1]
        ci[0] = 2.0 * s
        sys.stdout.write(" ".join(fmtv(v) for v in ci) + "\n")
    else:
        n = int(toks[1])
        c = [float(v) for v in toks[2:2 + n]]
        d = [0.0] * n
        dd = [0.0] * n
        d[0] = c[n - 1]
        for j in range(n - 2, 0, -1):
            for k in range(n - j, 0, -1):
                sv = d[k]
                d[k] = 2.0 * d[k - 1] - dd[k]
                dd[k] = sv
            sv = d[0]
            d[0] = -dd[0] + c[j]
            dd[0] = sv
        for j in range(n - 1, 0, -1):
            d[j] = d[j - 1] - dd[j]
        d[0] = -dd[0] + 0.5 * c[0]
        sys.stdout.write(" ".join(fmtv(v) for v in d) + "\n")


main()
