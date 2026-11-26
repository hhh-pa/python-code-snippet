# Elementary quadrature (NR 4.2).
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
    a = float(toks[rest])
    b = float(toks[rest + 1])

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
        return p[0] * math.pow(p[1] * t + p[2], p[3])

    n = 0
    s = 0.0

    def nxt():
        nonlocal n, s
        n += 1
        if n == 1:
            s = 0.5 * (b - a) * (f(a) + f(b))
            return s
        it = 1
        for _ in range(1, n - 1):
            it <<= 1
        tnm = float(it)
        dl = (b - a) / tnm
        x = a + 0.5 * dl
        sm = 0.0
        for _ in range(it):
            sm += f(x)
            x += dl
        s = 0.5 * (s + (b - a) * sm / tnm)
        return s

    eps = 1.0e-10
    jmax = 20
    ans = 0.0
    if op == "TRAPZD":
        l = int(toks[rest + 2])
        for _ in range(l):
            ans = nxt()
    elif op == "QTRAP":
        olds = 0.0
        for j in range(jmax):
            ans = nxt()
            if j > 5:
                if abs(ans - olds) < eps * abs(olds) or (ans == 0.0 and olds == 0.0):
                    break
            olds = ans
    else:
        ost = 0.0
        os = 0.0
        for j in range(jmax):
            st = nxt()
            ans = (4.0 * st - ost) / 3.0
            if j > 5:
                if abs(ans - os) < eps * abs(os) or (ans == 0.0 and os == 0.0):
                    break
            os = ans
            ost = st
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
