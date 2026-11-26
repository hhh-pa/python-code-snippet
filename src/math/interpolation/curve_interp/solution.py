# Curve interpolation in multidimensions (NR 3.7.5).
import math
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def frad(a, b, dim):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def fprime(x, y, pm):
    n = len(x)
    e = 0 if pm == 1 else n - 1
    s1 = x[e] - x[e + pm * 1]
    s2 = x[e] - x[e + pm * 2]
    s3 = x[e] - x[e + pm * 3]
    s12, s13, s23 = s1 - s2, s1 - s3, s2 - s3
    return (-(s1 * s2 / (s13 * s23 * s3)) * y[e + pm * 3]
            + (s1 * s3 / (s12 * s2 * s23)) * y[e + pm * 2]
            - (s2 * s3 / (s1 * s12 * s13)) * y[e + pm * 1]
            + (1.0 / s1 + 1.0 / s2 + 1.0 / s3) * y[e])


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    cls = toks[0] == "CLOSED"
    n, dim = int(toks[1]), int(toks[2])
    nums = [float(v) for v in toks[3:]]
    ptsin = [nums[i * dim:(i + 1) * dim] for i in range(n)]
    q = int(nums[n * dim])
    qs = nums[n * dim + 1:n * dim + 1 + q]
    inn = 2 * n if cls else n
    ofs = n // 2 if cls else 0
    pts = [[0.0] * inn for _ in range(dim)]
    s = [0.0] * inn
    for i in range(inn):
        ii = (i - ofs) % n
        im = (ii - 1) % n
        for j in range(dim):
            pts[j][i] = ptsin[ii][j]
        if i > 0:
            s[i] = s[i - 1] + frad(ptsin[ii], ptsin[im], dim)
    ss = s[ofs + n] - s[ofs] if cls else s[n - 1] - s[0]
    soff = s[ofs]
    s = [(v - soff) / ss for v in s]
    nn = inn
    y2m = []
    for j in range(dim):
        db = 1.0e99 if inn < 4 else fprime(s, pts[j], 1)
        de = 1.0e99 if inn < 4 else fprime(s, pts[j], -1)
        y2 = [0.0] * nn
        u = [0.0] * (nn - 1)
        yv = pts[j]
        if db > 0.99e99:
            y2[0] = u[0] = 0.0
        else:
            y2[0] = -0.5
            u[0] = (3.0 / (s[1] - s[0])) * ((yv[1] - yv[0]) / (s[1] - s[0]) - db)
        for i in range(1, nn - 1):
            sig = (s[i] - s[i - 1]) / (s[i + 1] - s[i - 1])
            p = sig * y2[i - 1] + 2.0
            y2[i] = (sig - 1.0) / p
            ui = (yv[i + 1] - yv[i]) / (s[i + 1] - s[i]) - (yv[i] - yv[i - 1]) / (s[i] - s[i - 1])
            u[i] = (6.0 * ui / (s[i + 1] - s[i - 1]) - sig * u[i - 1]) / p
        if de > 0.99e99:
            qn = un = 0.0
        else:
            qn = 0.5
            un = (3.0 / (s[nn - 1] - s[nn - 2])) * (de - (yv[nn - 1] - yv[nn - 2]) / (s[nn - 1] - s[nn - 2]))
        y2[nn - 1] = (un - qn * u[nn - 2]) / (qn * y2[nn - 2] + 1.0)
        for k in range(nn - 2, -1, -1):
            y2[k] = y2[k] * y2[k + 1] + u[k]
        y2m.append(y2)
    out = []
    for t in qs:
        if cls:
            t = t - math.floor(t)
        row = []
        for j in range(dim):
            klo, khi = 0, nn - 1
            while khi - klo > 1:
                k = (khi + klo) >> 1
                if s[k] > t:
                    khi = k
                else:
                    klo = k
            jl = min(klo, nn - 2)
            h = s[jl + 1] - s[jl]
            a = (s[jl + 1] - t) / h
            b = (t - s[jl]) / h
            y = a * pts[j][jl] + b * pts[j][jl + 1] + ((a * a * a - a) * y2m[j][jl] + (b * b * b - b) * y2m[j][jl + 1]) * (h * h) / 6.0
            row.append(fmt(y))
        out.append(" ".join(row))
    print("\n".join(out))


main()
