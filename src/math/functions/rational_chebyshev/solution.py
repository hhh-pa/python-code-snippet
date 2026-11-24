# Rational Chebyshev approximation (NR 5.13, ratlsq).
import math
import sys


def fmtv(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def svdsolve(a, b):
    m = len(a)
    n = len(a[0])
    bb = [row[:] for row in a]
    v = [[0.0] * n for _ in range(n)]
    for i in range(n):
        v[i][i] = 1.0
    for _ in range(12):
        for p in range(n - 1):
            for q in range(p + 1, n):
                alpha = 0.0
                gamma = 0.0
                beta = 0.0
                for k in range(m):
                    alpha += bb[k][p] * bb[k][p]
                    gamma += bb[k][q] * bb[k][q]
                    beta += bb[k][p] * bb[k][q]
                if beta == 0.0:
                    continue
                zeta = (gamma - alpha) / (2.0 * beta)
                t = (-1.0 if zeta < 0.0 else 1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for k in range(m):
                    bp = bb[k][p]
                    bq = bb[k][q]
                    bb[k][p] = c * bp - s * bq
                    bb[k][q] = s * bp + c * bq
                for k in range(n):
                    vp = v[k][p]
                    vq = v[k][q]
                    v[k][p] = c * vp - s * vq
                    v[k][q] = s * vp + c * vq
    w = [0.0] * n
    u = [[0.0] * n for _ in range(m)]
    for j in range(n):
        s = 0.0
        for k in range(m):
            s += bb[k][j] * bb[k][j]
        w[j] = math.sqrt(s)
        if w[j] != 0.0:
            for k in range(m):
                u[k][j] = bb[k][j] / w[j]
    wmax = 0.0
    for j in range(n):
        if w[j] > wmax:
            wmax = w[j]
    thresh = 1.0e-13 * wmax
    tmp = [0.0] * n
    for j in range(n):
        s = 0.0
        if w[j] > thresh:
            for i in range(m):
                s += u[i][j] * b[i]
            s /= w[j]
        tmp[j] = s
    x = [0.0] * n
    for j in range(n):
        s = 0.0
        for jj in range(n):
            s += v[j][jj] * tmp[jj]
        x[j] = s
    return x


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
    a = float(toks[rest])
    b = float(toks[rest + 1])
    mm = int(toks[rest + 2])
    kk = int(toks[rest + 3])

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

    pio2 = math.pi / 2.0
    ncof = mm + kk + 1
    npt = 8 * ncof
    xs = [0.0] * npt
    for i in range(npt):
        if i < npt // 2 - 1:
            hth = pio2 * i / (npt - 1.0)
            sn = math.sin(hth)
            xs[i] = a + (b - a) * sn * sn
        else:
            hth = pio2 * (npt - i) / (npt - 1.0)
            sn = math.sin(hth)
            xs[i] = b - (b - a) * sn * sn
    fs = [f(x) for x in xs]
    wt = [1.0] * npt
    ee = [1.0] * npt
    best = [0.0] * ncof
    dev = 1.0e99
    e = 0.0
    for _ in range(5):
        u = [[0.0] * ncof for _ in range(npt)]
        bbv = [0.0] * npt
        for i in range(npt):
            power = wt[i]
            se = abs(e)
            if ee[i] < 0.0:
                se = -se
            bbv[i] = power * (fs[i] + se)
            for j in range(mm + 1):
                u[i][j] = power
                power *= xs[i]
            power = -bbv[i]
            for j in range(mm + 1, ncof):
                power *= xs[i]
                u[i][j] = power
        coff = svdsolve(u, bbv)
        devmax = 0.0
        total = 0.0
        for j in range(npt):
            num = 0.0
            den = 0.0
            for t in range(mm, -1, -1):
                num = num * xs[j] + coff[t]
            for t in range(kk, 0, -1):
                den = den * xs[j] + coff[mm + t]
            den = den * xs[j] + 1.0
            ee[j] = num / den - fs[j]
            wt[j] = abs(ee[j])
            total += wt[j]
            if wt[j] > devmax:
                devmax = wt[j]
        e = total / npt
        if devmax <= dev:
            dev = devmax
            best = list(coff)
    sys.stdout.write(" ".join(fmtv(v) for v in best[:mm + 1]) + "\n")
    sys.stdout.write(" ".join(fmtv(v) for v in best[mm + 1:]) + "\n")
    sys.stdout.write("%.6f\n" % (dev + 0.0))


main()
