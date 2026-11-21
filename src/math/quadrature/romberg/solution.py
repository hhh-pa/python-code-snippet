# Romberg integration (NR 4.3). Port of the C++ reference.
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
    elif fun == "POW":
        p = [float(v) for v in toks[1:5]]
        rest = 5
    else:
        p = [float(v) for v in toks[1:4]]
        rest = 4
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
        h[j] = 0.25 * h[j - 1]
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
