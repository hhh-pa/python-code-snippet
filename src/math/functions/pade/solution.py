# Pade approximants (NR 5.12).
import sys


def fmtv(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def lusolve(lu, p, rhs, n):
    y = [0.0] * n
    x = [0.0] * n
    for i in range(n):
        s = rhs[p[i]]
        for j in range(i):
            s -= lu[i][j] * y[j]
        y[i] = s
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
    c = [float(v) for v in toks[1:2 + 2 * n]]
    a0 = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for k in range(1, n + 1):
        for m in range(1, n + 1):
            a0[k - 1][m - 1] = c[n - m + k]
        rhs[k - 1] = -c[n + k]
    lu = [row[:] for row in a0]
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
    bb = lusolve(lu, p, rhs, n)
    r = [0.0] * n
    for i in range(n):
        s = -rhs[i]
        for j in range(n):
            s += a0[i][j] * bb[j]
        r[i] = s
    dx = lusolve(lu, p, r, n)
    for i in range(n):
        bb[i] -= dx[i]
    b = [0.0] * (n + 1)
    b[0] = 1.0
    for m in range(1, n + 1):
        b[m] = bb[m - 1]
    av = [0.0] * (n + 1)
    av[0] = c[0]
    for k in range(1, n + 1):
        s = 0.0
        for m in range(k + 1):
            s += b[m] * c[k - m]
        av[k] = s
    sys.stdout.write(" ".join(fmtv(v) for v in av) + "\n")
    sys.stdout.write(" ".join(fmtv(v) for v in b[1:]) + "\n")


main()
