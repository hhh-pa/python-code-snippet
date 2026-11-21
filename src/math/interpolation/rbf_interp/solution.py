# Radial basis function interpolation (NR 3.7). Port of the C++ reference.
import math
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    r0 = float(toks[1])
    normflag = int(toks[2])
    n = int(toks[3])
    dim = int(toks[4])
    nums = [float(v) for v in toks[5:]]
    pts = [nums[i * dim:(i + 1) * dim] for i in range(n)]
    vals = nums[n * dim:n * dim + n]
    q = int(nums[n * dim + n])
    qs = [nums[n * dim + n + 1 + i * dim:n * dim + n + 1 + (i + 1) * dim] for i in range(q)]

    def phi(r):
        if op == "MULTIQUADRIC":
            return math.sqrt(r * r + r0 * r0)
        if op == "THINPLATE":
            return 0.0 if r <= 0.0 else r * r * math.log(r / r0)
        if op == "GAUSS":
            t = r / r0
            return math.exp(-0.5 * t * t)
        return 1.0 / math.sqrt(r * r + r0 * r0)

    def rad(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    phim = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(n):
            v = phi(rad(pts[i], pts[j]))
            phim[i][j] = v
            s += v
        rhs[i] = s * vals[i] if normflag else vals[i]
    p = list(range(n))
    for k in range(n):
        piv = k
        for i in range(k + 1, n):
            if abs(phim[i][k]) > abs(phim[piv][k]):
                piv = i
        if piv != k:
            phim[k], phim[piv] = phim[piv], phim[k]
            p[k], p[piv] = p[piv], p[k]
        for i in range(k + 1, n):
            phim[i][k] /= phim[k][k]
            for j in range(k + 1, n):
                phim[i][j] -= phim[i][k] * phim[k][j]
    y = [0.0] * n
    for i in range(n):
        s = rhs[p[i]]
        for j in range(i):
            s -= phim[i][j] * y[j]
        y[i] = s
    w = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= phim[i][j] * w[j]
        w[i] = s / phim[i][i]
    out = []
    for pt in qs:
        sumw = sums = 0.0
        for i in range(n):
            f = phi(rad(pt, pts[i]))
            sumw += w[i] * f
            sums += f
        out.append(fmt(sumw / sums if normflag else sumw))
    print("\n".join(out))


main()
