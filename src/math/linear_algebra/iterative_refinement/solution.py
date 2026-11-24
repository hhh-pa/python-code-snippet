# Iterative refinement of a linear solve (NR 2.5, mprove).
#
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def lusolve(lu, p, rhs):
    n = len(lu)
    y = [0.0] * n
    for i in range(n):
        s = rhs[p[i]]
        for j in range(i):
            s -= lu[i][j] * y[j]
        y[i] = s
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= lu[i][j] * x[j]
        x[i] = s / lu[i][i]
    return x


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    nums = [float(v) for v in toks[1:]]
    a = [nums[i * n:(i + 1) * n] for i in range(n)]
    b = nums[n * n:n * n + n]
    lu = [row[:] for row in a]
    p = list(range(n))
    for k in range(n):
        piv = k
        for i in range(k + 1, n):
            if abs(lu[i][k]) > abs(lu[piv][k]):
                piv = i
        if piv != k:
            lu[k], lu[piv] = lu[piv], lu[k]
            p[k], p[piv] = p[piv], p[k]
        for i in range(k + 1, n):
            lu[i][k] /= lu[k][k]
            for j in range(k + 1, n):
                lu[i][j] -= lu[i][k] * lu[k][j]
    x = lusolve(lu, p, b)
    for _ in range(2):
        r = [0.0] * n
        for i in range(n):
            s = -b[i]
            c = 0.0
            for j in range(n):
                y = a[i][j] * x[j] - c
                t = s + y
                c = (t - s) - y
                s = t
            r[i] = s
        dx = lusolve(lu, p, r)
        x = [xi - dxi for xi, dxi in zip(x, dx)]
    print(" ".join(fmt(v) for v in x))


main()
