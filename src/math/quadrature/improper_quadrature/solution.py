# Improper integrals (NR 4.4). Port of the C++ reference.
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

    def num(t):
        if t == "INF":
            return 1.0e99
        if t == "-INF":
            return -1.0e99
        return float(t)

    ain = num(toks[rest])
    bin = num(toks[rest + 1])

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

    if op == "MIDINF":
        a, b = 1.0 / bin, 1.0 / ain
    elif op == "MIDEXP":
        a, b = 0.0, math.exp(-ain)
    elif op in ("MIDSQL", "MIDSQU"):
        a, b = 0.0, math.sqrt(bin - ain)
    else:
        a, b = ain, bin

    def g(x):
        if op == "MIDPNT":
            return f(x)
        if op == "MIDINF":
            return f(1.0 / x) / (x * x)
        if op == "MIDEXP":
            return f(-math.log(x)) / x
        if op == "MIDSQL":
            return 2.0 * x * f(ain + x * x)
        return 2.0 * x * f(bin - x * x)

    n = 0
    s = 0.0

    def nxt():
        nonlocal n, s
        n += 1
        if n == 1:
            s = (b - a) * g(0.5 * (a + b))
            return s
        it = 1
        for _ in range(1, n - 1):
            it *= 3
        tnm = float(it)
        dl = (b - a) / (3.0 * tnm)
        ddel = dl + dl
        x = a + 0.5 * dl
        sm = 0.0
        for _ in range(it):
            sm += g(x)
            x += ddel
            sm += g(x)
            x += dl
        s = (s + (b - a) * sm / tnm) / 3.0
        return s

    eps = 3.0e-9
    jmax = 14
    k = 5
    ss = [0.0] * jmax
    h = [0.0] * (jmax + 1)
    h[0] = 1.0
    ans = 0.0
    for j in range(1, jmax + 1):
        ss[j - 1] = nxt()
        if j >= k:
            c = [0.0] * k
            d = [0.0] * k
            dif = abs(0.0 - h[j - k])
            ns = 0
            for i in range(k):
                dift = abs(0.0 - h[j - k + i])
                if dift < dif:
                    ns = i
                    dif = dift
                c[i] = ss[j - k + i]
                d[i] = ss[j - k + i]
            y = ss[j - k + ns]
            ns -= 1
            dy = 0.0
            for mm in range(1, k):
                for i in range(k - mm):
                    ho = h[j - k + i]
                    hp = h[j - k + i + mm]
                    w = c[i + 1] - d[i]
                    den = w / (ho - hp)
                    d[i] = hp * den
                    c[i] = ho * den
                if 2 * (ns + 1) < k - mm:
                    dy = c[ns + 1]
                else:
                    dy = d[ns]
                    ns -= 1
                y += dy
            if abs(dy) <= eps * abs(y):
                ans = y
                break
            ans = y
        h[j] = h[j - 1] / 9.0
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
