# Singular value decomposition (NR 2.6 contract): one-sided Jacobi.
#
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
    m, n = int(toks[1]), int(toks[2])
    nums = [float(v) for v in toks[3:]]
    a = [nums[i * n:(i + 1) * n] for i in range(m)]
    pos = m * n
    b, thresh = [], 0.0
    if op == "SOLVE":
        b = nums[pos:pos + m]
        thresh = nums[pos + m]
    if op in ("RANK", "SUBSPACE"):
        thresh = nums[pos]
    bb = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(12):
        for p in range(n - 1):
            for q in range(p + 1, n):
                alpha = gamma = beta = 0.0
                for k in range(m):
                    alpha += bb[k][p] * bb[k][p]
                    gamma += bb[k][q] * bb[k][q]
                    beta += bb[k][p] * bb[k][q]
                if beta == 0.0:
                    continue
                zeta = (gamma - alpha) / (2.0 * beta)
                t = ((-1.0 if zeta < 0.0 else 1.0)
                     / (abs(zeta) + math.sqrt(1.0 + zeta * zeta)))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for k in range(m):
                    bp, bq = bb[k][p], bb[k][q]
                    bb[k][p] = c * bp - s * bq
                    bb[k][q] = s * bp + c * bq
                for k in range(n):
                    vp, vq = v[k][p], v[k][q]
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
    for i in range(n - 1):
        best = i
        for j in range(i + 1, n):
            if w[j] > w[best]:
                best = j
        if best != i:
            w[i], w[best] = w[best], w[i]
            for k in range(m):
                u[k][i], u[k][best] = u[k][best], u[k][i]
            for k in range(n):
                v[k][i], v[k][best] = v[k][best], v[k][i]
    if op == "FACTOR":
        print("U")
        for i in range(m):
            print(" ".join(fmt(u[i][j]) for j in range(n)))
        print("W")
        print(" ".join(fmt(w[j]) for j in range(n)))
        print("V")
        for i in range(n):
            print(" ".join(fmt(v[i][j]) for j in range(n)))
        return
    if op == "SOLVE":
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
        print(" ".join(fmt(v) for v in x))
        return
    if op == "RANK":
        rank = sum(1 for j in range(n) if w[j] > thresh)
        print(f"{rank} {n - rank}")
        return
    if op == "SUBSPACE":
        rg = [j for j in range(n) if w[j] > thresh]
        ns = [j for j in range(n) if w[j] <= thresh]
        print(f"RANGE {len(rg)}")
        for j in rg:
            print(" ".join(fmt(u[i][j]) for i in range(m)))
        print(f"NULLSPACE {len(ns)}")
        for j in ns:
            print(" ".join(fmt(v[i][j]) for i in range(n)))
        return
    cnd = 0.0 if (w[0] <= 0.0 or w[n - 1] <= 0.0) else w[n - 1] / w[0]
    print(fmt(cnd))


main()
