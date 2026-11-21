# Sparse linear systems (NR 2.7): CCS matvecs + BiCG.
# Port of the C++ reference.
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
    n, nnz = int(toks[1]), int(toks[2])
    raw = toks[3:]
    trips = sorted([(int(raw[k * 3 + 1]), int(raw[k * 3]), float(raw[k * 3 + 2]))
                    for k in range(nnz)])
    col_ptr = [0] * (n + 1)
    for j, _, _ in trips:
        col_ptr[j + 1] += 1
    for j in range(n):
        col_ptr[j + 1] += col_ptr[j]
    row_ind = [0] * nnz
    val = [0.0] * nnz
    nxt = col_ptr[:]
    for j, i, v in trips:
        k = nxt[j]
        nxt[j] += 1
        row_ind[k] = i
        val[k] = v

    def ax(x):
        y = [0.0] * n
        for j in range(n):
            for i in range(col_ptr[j], col_ptr[j + 1]):
                y[row_ind[i]] += val[i] * x[j]
        return y

    def atx(x):
        y = [0.0] * n
        for i in range(n):
            y[i] = 0.0
            for j in range(col_ptr[i], col_ptr[i + 1]):
                y[i] += val[j] * x[row_ind[j]]
        return y

    diag = [0.0] * n
    for i in range(n):
        for j in range(col_ptr[i], col_ptr[i + 1]):
            if row_ind[j] == i:
                diag[i] = val[j]
                break

    def asolve(b):
        return [b[i] / diag[i] if diag[i] != 0.0 else b[i] for i in range(n)]

    def dot(a, b):
        s = 0.0
        for i in range(n):
            s += a[i] * b[i]
        return s

    rest = raw[nnz * 3:]
    if op in ("MATVEC", "TMATVEC"):
        x = [float(v) for v in rest[:n]]
        y = ax(x) if op == "MATVEC" else atx(x)
        print(" ".join(fmt(v) for v in y))
        return
    b = [float(v) for v in rest[:n]]
    itmax = int(rest[n])
    x = [0.0] * n
    p = [0.0] * n
    pp = [0.0] * n
    ax0 = ax(x)
    r = [b[j] - ax0[j] for j in range(n)]
    rr = list(r)
    z = asolve(r)
    bkden = 1.0
    for it in range(1, itmax + 1):
        zz = asolve(rr)
        bknum = dot(z, rr)
        if it == 1:
            p, pp = list(z), list(zz)
        else:
            bk = 0.0 if bkden == 0.0 else bknum / bkden
            p = [bk * p[j] + z[j] for j in range(n)]
            pp = [bk * pp[j] + zz[j] for j in range(n)]
        bkden = bknum
        z = ax(p)
        akden = dot(z, pp)
        ak = 0.0 if akden == 0.0 else bknum / akden
        zz = atx(pp)
        x = [x[j] + ak * p[j] for j in range(n)]
        r = [r[j] - ak * z[j] for j in range(n)]
        rr = [rr[j] - ak * zz[j] for j in range(n)]
        z = asolve(r)
    axf = ax(x)
    rn = 0.0
    for j in range(n):
        d = b[j] - axf[j]
        rn += d * d
    print(" ".join(fmt(v) for v in x))
    print(fmt(math.sqrt(rn)))


main()
