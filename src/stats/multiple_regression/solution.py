"""OLS multiple regression (Think Stats 2e ch 11)."""

import sys


def _normal_equations(rows, p, k):
    mat = [[0.0] * k for _ in range(k)]
    vec = [0.0] * k
    for row in rows:
        cols = [1.0] + [float(v) for v in row[:p]]
        y = float(row[p])
        for i in range(k):
            for j in range(k):
                mat[i][j] += cols[i] * cols[j]
            vec[i] += cols[i] * y
    return mat, vec


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


def _rsq(rows, beta, p, k):
    n = len(rows)
    my = sum(r[p] for r in rows) / n
    ssres = 0.0
    sstot = 0.0
    for row in rows:
        pred = beta[0]
        for j in range(1, k):
            pred += beta[j] * row[j - 1]
        r = row[p] - pred
        ssres += r * r
        d = row[p] - my
        sstot += d * d
    return 0.0 if sstot == 0.0 else 1 - ssres / sstot


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    p = int(toks[1])
    k = p + 1
    rows = []
    idx = 2
    for _ in range(n):
        rows.append(list(map(int, toks[idx : idx + p + 1])))
        idx += p + 1
    mat, vec = _normal_equations(rows, p, k)
    beta = _gauss_solve(mat, vec, k)
    if beta is None:
        sys.stdout.write("SINGULAR")
        return
    r2 = _rsq(rows, beta, p, k)
    out = "BETA " + " ".join(f"{b:.6f}" for b in beta) + f"\nRSQ {r2:.6f}"
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
