# Grid interpolation (NR 3.6).
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def locate(xx, x):
    n = len(xx)
    klo, khi = 0, n - 1
    while khi - klo > 1:
        k = (khi + klo) >> 1
        if xx[k] > x:
            khi = k
        else:
            klo = k
    return min(klo, n - 2)


def neville(xa, ya, m, x):
    c = list(ya[:m])
    d = list(ya[:m])
    dif = abs(x - xa[0])
    ns = 0
    for i in range(m):
        dift = abs(x - xa[i])
        if dift < dif:
            ns = i
            dif = dift
    y = ya[ns]
    ns -= 1
    for mm in range(1, m):
        for i in range(m - mm):
            ho = xa[i] - x
            hp = xa[i + mm] - x
            w = c[i + 1] - d[i]
            den = w / (ho - hp)
            d[i] = hp * den
            c[i] = ho * den
        if 2 * (ns + 1) < (m - mm):
            y += c[ns + 1]
        else:
            y += d[ns]
            ns -= 1
    return y


def spline_y2(xv, yv):
    n = len(xv)
    y2 = [0.0] * n
    u = [0.0] * (n - 1)
    y2[0] = u[0] = 0.0
    for i in range(1, n - 1):
        sig = (xv[i] - xv[i - 1]) / (xv[i + 1] - xv[i - 1])
        p = sig * y2[i - 1] + 2.0
        y2[i] = (sig - 1.0) / p
        ui = (yv[i + 1] - yv[i]) / (xv[i + 1] - xv[i]) - (yv[i] - yv[i - 1]) / (xv[i] - xv[i - 1])
        u[i] = (6.0 * ui / (xv[i + 1] - xv[i - 1]) - sig * u[i - 1]) / p
    y2[n - 1] = 0.0
    for k in range(n - 2, -1, -1):
        y2[k] = y2[k] * y2[k + 1] + u[k]
    return y2


def splint(xv, yv, y2, x):
    jl = locate(xv, x)
    h = xv[jl + 1] - xv[jl]
    a = (xv[jl + 1] - x) / h
    b = (x - xv[jl]) / h
    return a * yv[jl] + b * yv[jl + 1] + ((a * a * a - a) * y2[jl] + (b * b * b - b) * y2[jl + 1]) * (h * h) / 6.0


WT = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [-3, 0, 0, 3, 0, 0, 0, 0, -2, 0, 0, -1, 0, 0, 0, 0],
    [2, 0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, -3, 0, 0, 3, 0, 0, 0, 0, -2, 0, 0, -1],
    [0, 0, 0, 0, 2, 0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 1],
    [-3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0],
    [9, -9, 9, -9, 6, 3, -3, -6, 6, -6, -3, 3, 4, 2, 1, 2],
    [-6, 6, -6, 6, -4, -2, 2, 4, -3, 3, 3, -3, -2, -1, -1, -2],
    [2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0],
    [-6, 6, -6, 6, -3, -3, 3, 3, -4, 4, 2, -2, -2, -2, -1, -1],
    [4, -4, 4, -4, 2, 2, -2, -2, 2, -2, -2, 2, 1, 1, 1, 1],
]


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    out = []
    if op == "BICUBIC":
        nums = [float(v) for v in toks[1:]]
        x1l, x1u, x2l, x2u = nums[0], nums[1], nums[2], nums[3]
        y, y1 = nums[4:8], nums[8:12]
        y2, y12 = nums[12:16], nums[16:20]
        q = int(nums[20])
        qs = nums[21:]
        d1, d2 = x1u - x1l, x2u - x2l
        d1d2 = d1 * d2
        x = [0.0] * 16
        for i in range(4):
            x[i] = y[i]
            x[i + 4] = y1[i] * d1
            x[i + 8] = y2[i] * d2
            x[i + 12] = y12[i] * d1d2
        c = [[0.0] * 4 for _ in range(4)]
        for i in range(16):
            xx = 0.0
            for k in range(16):
                xx += WT[i][k] * x[k]
            c[i // 4][i % 4] = xx
        for qq in range(q):
            x1, x2 = qs[2 * qq], qs[2 * qq + 1]
            t = (x1 - x1l) / d1
            u = (x2 - x2l) / d2
            ansy = ansy1 = ansy2 = 0.0
            for i in range(3, -1, -1):
                ansy = t * ansy + ((c[i][3] * u + c[i][2]) * u + c[i][1]) * u + c[i][0]
                ansy2 = t * ansy2 + (3.0 * c[i][3] * u + 2.0 * c[i][2]) * u + c[i][1]
                ansy1 = u * ansy1 + (3.0 * c[3][i] * t + 2.0 * c[2][i]) * t + c[1][i]
            ansy1 /= d1
            ansy2 /= d2
            out.append(f"{fmt(ansy)} {fmt(ansy1)} {fmt(ansy2)}")
        print("\n".join(out))
        return
    p = 1
    m, n = int(toks[p]), int(toks[p + 1])
    p += 2
    x1v = [float(v) for v in toks[p:p + m]]
    p += m
    x2v = [float(v) for v in toks[p:p + n]]
    p += n
    ym = []
    for _ in range(m):
        ym.append([float(v) for v in toks[p:p + n]])
        p += n
    mm = nn = 0
    if op == "POLY2D":
        mm, nn = int(toks[p]), int(toks[p + 1])
        p += 2
    q = int(toks[p])
    p += 1
    qs = [(float(toks[p + 2 * i]), float(toks[p + 2 * i + 1])) for i in range(q)]
    rowy2 = [spline_y2(x2v, ym[i]) for i in range(m)] if op == "SPLINE2D" else []
    for x1p, x2p in qs:
        if op == "BILINEAR":
            i, j = locate(x1v, x1p), locate(x2v, x2p)
            t = (x1p - x1v[i]) / (x1v[i + 1] - x1v[i])
            u = (x2p - x2v[j]) / (x2v[j + 1] - x2v[j])
            ans = (1 - t) * (1 - u) * ym[i][j] + t * (1 - u) * ym[i + 1][j] \
                + (1 - t) * u * ym[i][j + 1] + t * u * ym[i + 1][j + 1]
        elif op == "POLY2D":
            klo, khi = 0, m - 1
            while khi - klo > 1:
                k = (khi + klo) >> 1
                if x1v[k] > x1p:
                    khi = k
                else:
                    klo = k
            bi = max(0, min(m - mm, klo - ((mm - 2) >> 1)))
            klo, khi = 0, n - 1
            while khi - klo > 1:
                k = (khi + klo) >> 1
                if x2v[k] > x2p:
                    khi = k
                else:
                    klo = k
            bj = max(0, min(n - nn, klo - ((nn - 2) >> 1)))
            yv = [0.0] * m
            for k in range(bi, bi + mm):
                xs = x2v[bj:bj + nn]
                ys = ym[k][bj:bj + nn]
                yv[k] = neville(xs, ys, nn, x2p)
            ans = neville(x1v[bi:bi + mm], [yv[bi + k] for k in range(mm)], mm, x1p)
        else:
            yv = [splint(x2v, ym[i], rowy2[i], x2p) for i in range(m)]
            ans = splint(x1v, yv, spline_y2(x1v, yv), x1p)
        out.append(fmt(ans))
    print("\n".join(out))


main()
