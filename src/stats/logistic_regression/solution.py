"""Logistic regression by IRLS (Think Stats 2e ch 11)."""

import math
import sys


def _gauss_solve(mat, vec, k):
    for s in range(k):
        piv = s
        for r in range(s + 1, k):
            if abs(mat[r][s]) > abs(mat[piv][s]):
                piv = r
        mat[s], mat[piv] = mat[piv], mat[s]
        vec[s], vec[piv] = vec[piv], vec[s]
        if mat[s][s] == 0.0:
            return None
        for r in range(s + 1, k):
            factor = mat[r][s] / mat[s][s]
            for ccol in range(s, k):
                mat[r][ccol] -= factor * mat[s][ccol]
            vec[r] -= factor * vec[s]
    beta = [0.0] * k
    for s in range(k - 1, -1, -1):
        tot = vec[s]
        for ccol in range(s + 1, k):
            tot -= mat[s][ccol] * beta[ccol]
        beta[s] = tot / mat[s][s]
    return beta


def _irls_matrix(rows, beta, p, k):
    mat = [[0.0] * k for _ in range(k)]
    vec = [0.0] * k
    for row in rows:
        cols = [1.0] + [float(v) for v in row[:p]]
        lin = 0.0
        for j in range(k):
            lin += cols[j] * beta[j]
        pr = 1 / (1 + math.exp(-lin))
        w = pr * (1 - pr)
        if w == 0.0:
            continue
        z = lin + (row[p] - pr) / w
        for i in range(k):
            for j in range(k):
                mat[i][j] += w * cols[i] * cols[j]
            vec[i] += w * z * cols[i]
    return mat, vec


def _accuracy(rows, beta, p, k):
    good = 0
    for row in rows:
        lin = beta[0]
        for j in range(1, k):
            lin += beta[j] * row[j - 1]
        pr = 1 / (1 + math.exp(-lin))
        if (pr >= 0.5) == (row[p] == 1):
            good += 1
    return good


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    p = int(toks[1])
    t = int(toks[2])
    k = p + 1
    rows = []
    idx = 3
    for _ in range(n):
        rows.append(list(map(int, toks[idx : idx + p + 1])))
        idx += p + 1
    beta = [0.0] * k
    for _ in range(t):
        mat, vec = _irls_matrix(rows, beta, p, k)
        beta = _gauss_solve(mat, vec, k)
        if beta is None:
            sys.stdout.write("SINGULAR")
            return
    good = _accuracy(rows, beta, p, k)
    out = "BETA " + " ".join(f"{b:.6f}" for b in beta) + f"\nACC {good / n:.6f}"
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
