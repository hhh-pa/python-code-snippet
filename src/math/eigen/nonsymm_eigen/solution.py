# Nonsymmetric eigensystem preprocessing toolkit: Osborne balancing
# (balance/balbak) and reduction to upper Hessenberg form by the
# elimination method (elmhes) with accumulated transformation (eltran).
# Reference: Press et al., Numerical Recipes 3e, Section 11.6.
# The QR iteration for Hessenberg matrices (11.7: hqr/hqr2/sort/sortvecs)
# is Webnote-only (Webnote 17), not in the book, so eigenvalues and
# eigenvectors of general nonsymmetric matrices are not computed here.
# Documented decisions: RADIX is hardcoded to 2.0 (the book derives
# numeric_limits<Doub>::radix, "2 for all modern machines"); perm[0] and
# perm[n-1] are unset by the book (only 1..n-2 defined), so we
# emit identity there for determinism (eltran never reads them).
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import sys


def balance(a, scale):
    n = len(a)
    radix = 2.0
    done = False
    sqrdx = radix * radix
    while not done:
        done = True
        for i in range(n):
            r = 0.0
            c = 0.0
            for j in range(n):
                if j != i:
                    c += abs(a[j][i])
                    r += abs(a[i][j])
            if c != 0.0 and r != 0.0:
                g = r / radix
                f = 1.0
                s = c + r
                while c < g:
                    f *= radix
                    c *= sqrdx
                g = r * radix
                while c > g:
                    f /= radix
                    c /= sqrdx
                if (c + r) / f < 0.95 * s:
                    done = False
                    g = 1.0 / f
                    scale[i] *= f
                    for j in range(n):
                        a[i][j] *= g
                    for j in range(n):
                        a[j][i] *= f


def balbak(zz, scale):
    n = len(zz)
    for i in range(n):
        for j in range(n):
            zz[i][j] *= scale[i]


def elmhes(a, perm):
    n = len(a)
    for m in range(1, n - 1):
        x = 0.0
        i = m
        for j in range(m, n):
            if abs(a[j][m - 1]) > abs(x):
                x = a[j][m - 1]
                i = j
        perm[m] = i
        if i != m:
            for j in range(m - 1, n):
                t = a[i][j]
                a[i][j] = a[m][j]
                a[m][j] = t
            for j in range(n):
                t = a[j][i]
                a[j][i] = a[j][m]
                a[j][m] = t
        if x != 0.0:
            for i in range(m + 1, n):
                y = a[i][m - 1]
                if y != 0.0:
                    y /= x
                    a[i][m - 1] = y
                    for j in range(m, n):
                        a[i][j] -= y * a[m][j]
                    for j in range(n):
                        a[j][m] += y * a[j][i]


def eltran(a, perm, zz):
    n = len(a)
    for i in range(n):
        for j in range(n):
            zz[i][j] = 1.0 if i == j else 0.0
    for mp in range(n - 2, 0, -1):
        for k in range(mp + 1, n):
            zz[k][mp] = a[k][mp - 1]
        i = perm[mp]
        if i != mp:
            for j in range(mp, n):
                zz[mp][j] = zz[i][j]
                zz[i][j] = 0.0
            zz[i][mp] = 1.0


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def read_mat(toks, p, n):
    vals = [float(t) for t in toks[p:p + n * n]]
    return [vals[i * n:(i + 1) * n] for i in range(n)], p + n * n


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    if op == "BALANCE":
        a, _ = read_mat(toks, 2, n)
        scale = [1.0] * n
        balance(a, scale)
        parts = [fmt6(a[i][j]) for i in range(n) for j in range(n)]
        parts += [fmt6(v) for v in scale]
        print(" ".join(parts))
    elif op == "HESSENBERG":
        a, _ = read_mat(toks, 2, n)
        perm = list(range(n))
        elmhes(a, perm)
        parts = [fmt6(a[i][j]) for i in range(n) for j in range(n)]
        parts += [str(v) for v in perm]
        print(" ".join(parts))
    elif op == "ELTRAN":
        a, p = read_mat(toks, 2, n)
        perm = [int(t) for t in toks[p:p + n]]
        zz = [[0.0] * n for _ in range(n)]
        eltran(a, perm, zz)
        parts = [fmt6(zz[i][j]) for i in range(n) for j in range(n)]
        print(" ".join(parts))
    elif op == "BALBAK":
        zz, p = read_mat(toks, 2, n)
        scale = [float(t) for t in toks[p:p + n]]
        balbak(zz, scale)
        parts = [fmt6(zz[i][j]) for i in range(n) for j in range(n)]
        print(" ".join(parts))


main()
