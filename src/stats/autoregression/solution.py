"""Autoregression AR(p) fit + forecast (Think Stats 2e ch 12)."""

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


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    p = int(toks[1])
    f = int(toks[2])
    xs = list(map(int, toks[3 : 3 + n]))
    k = p + 1
    mat = [[0.0] * k for _ in range(k)]
    vec = [0.0] * k
    for t in range(p, n):
        cols = [1.0] + [float(xs[t - j]) for j in range(1, k)]
        y = float(xs[t])
        for i in range(k):
            for j in range(k):
                mat[i][j] += cols[i] * cols[j]
            vec[i] += cols[i] * y
    beta = _gauss_solve(mat, vec, k)
    if beta is None:
        sys.stdout.write("SINGULAR")
        return
    hist = [float(v) for v in xs]
    outs = []
    for _ in range(f):
        pred = beta[0]
        for j in range(1, k):
            pred += beta[j] * hist[len(hist) - j]
        hist.append(pred)
        outs.append(f"{pred:.6f}")
    out = "BETA " + " ".join(f"{b:.6f}" for b in beta) + "\nFORECAST " + " ".join(outs)
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
