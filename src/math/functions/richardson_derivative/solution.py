# Numerical derivative (NR 5.7, Ridders' method). Port of the C++ reference.
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    fun = toks[0]
    if fun == "POLY":
        d = int(toks[1])
        p = [float(v) for v in toks[2:3 + d]]
        rest = 3 + d
    else:
        p = [float(v) for v in toks[1:4]]
        rest = 4
    x = float(toks[rest])
    h = float(toks[rest + 1])

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

    con = 1.4
    con2 = con * con
    big = 1.0e30
    ntab = 10
    a = [[0.0] * ntab for _ in range(ntab)]
    a[0][0] = (f(x + h) - f(x - h)) / (2.0 * h)
    err = big
    ans = a[0][0]
    for i in range(1, ntab):
        h /= con
        a[0][i] = (f(x + h) - f(x - h)) / (2.0 * h)
        fac = con2
        for j in range(1, i + 1):
            a[j][i] = (a[j - 1][i] * fac - a[j - 1][i - 1]) / (fac - 1.0)
            fac *= con2
            errt = abs(a[j][i] - a[j - 1][i])
            e2 = abs(a[j][i] - a[j - 1][i - 1])
            if e2 > errt:
                errt = e2
            if errt <= err:
                err = errt
                ans = a[j][i]
    if abs(ans) < 5e-7:
        ans = 0.0
    if abs(err) < 5e-7:
        err = 0.0
    sys.stdout.write("%.6f %.6f\n" % (ans + 0.0, err + 0.0))


main()
