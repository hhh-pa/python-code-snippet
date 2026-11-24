# Kriging interpolation (NR 3.7.6).
import math
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    beta = float(toks[0])
    nug = float(toks[1])
    n = int(toks[2])
    dim = int(toks[3])
    nums = [float(v) for v in toks[4:]]
    pts = [nums[i * dim:(i + 1) * dim] for i in range(n)]
    vals = nums[n * dim:n * dim + n]
    q = int(nums[n * dim + n])
    qs = [nums[n * dim + n + 1 + i * dim:n * dim + n + 1 + (i + 1) * dim] for i in range(q)]
    nugsq = nug * nug

    def rdist(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    num = den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            rb = sum((pts[i][k] - pts[j][k]) ** 2 for k in range(dim))
            rb = rb ** (0.5 * beta)
            num += rb * (0.5 * (vals[i] - vals[j]) ** 2 - nugsq)
            den += rb * rb
    alph = num / den

    def vgram(r):
        return nugsq + alph * (r ** beta)

    m = n + 1
    v = [[0.0] * m for _ in range(m)]
    y = [0.0] * m
    for i in range(n):
        y[i] = vals[i]
        for j in range(i, n):
            g = vgram(rdist(pts[i], pts[j]))
            v[i][j] = g
            v[j][i] = g
        v[i][n] = 1.0
        v[n][i] = 1.0
    p = list(range(m))
    for k in range(m):
        piv = k
        for i in range(k + 1, m):
            if abs(v[i][k]) > abs(v[piv][k]):
                piv = i
        if piv != k:
            v[k], v[piv] = v[piv], v[k]
            p[k], p[piv] = p[piv], p[k]
        for i in range(k + 1, m):
            v[i][k] /= v[k][k]
            for j in range(k + 1, m):
                v[i][j] -= v[i][k] * v[k][j]

    def lusolve(rhs):
        yy = [0.0] * m
        for i in range(m):
            s = rhs[p[i]]
            for j in range(i):
                s -= v[i][j] * yy[j]
            yy[i] = s
        x = [0.0] * m
        for i in range(m - 1, -1, -1):
            s = yy[i]
            for j in range(i + 1, m):
                s -= v[i][j] * x[j]
            x[i] = s / v[i][i]
        return x

    yvi = lusolve(y)
    out = []
    for pt in qs:
        vstar = [vgram(rdist(pt, pts[i])) for i in range(n)] + [1.0]
        lastval = sum(a * b for a, b in zip(yvi, vstar))
        dstar = lusolve(vstar)
        lasterr = sum(a * b for a, b in zip(dstar, vstar))
        out.append(f"{fmt(lastval)} {fmt(math.sqrt(max(0.0, lasterr)))}")
    print("\n".join(out))


main()
