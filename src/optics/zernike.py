"""Zernike fit + RMS (geom ch 13)."""

import math
import sys


def _snap(x):
    return 0.0 if abs(x) < 5e-7 else x


def _fact(n):
    f = 1
    for i in range(2, n + 1):
        f *= i
    return f


def _nm(j):
    n = 0
    while (n + 1) * (n + 2) // 2 < j:
        n += 1
    r = j - n * (n + 1) // 2 - 1
    if n % 2 == 0:
        if r == 0:
            m = 0
        elif r % 2 == 1:
            m = r + 1
        else:
            m = -r
    elif r % 2 == 0:
        m = r + 1
    else:
        m = -r
    return n, m


def _radial(n, m, ro):
    am = abs(m)
    tot = 0.0
    for s in range((n - am) // 2 + 1):
        num = _fact(n - s)
        den = _fact(s) * _fact((n + am) // 2 - s) * _fact((n - am) // 2 - s)
        pw = 1.0
        for _ in range(n - 2 * s):
            pw *= ro
        term = num / den * pw
        tot += term if s % 2 == 0 else -term
    return tot


def _zernike(j, ro, th):
    n, m = _nm(j)
    r = _radial(n, m, ro)
    if m == 0:
        return math.sqrt(n + 1) * r
    if m > 0:
        return math.sqrt(2 * (n + 1)) * r * math.cos(m * th)
    return math.sqrt(2 * (n + 1)) * r * math.sin(-m * th)


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
    jn = int(toks[0])
    n = int(toks[1])
    ros = [0.0] * n
    ths = [0.0] * n
    ws = [0.0] * n
    for i in range(n):
        ros[i] = float(toks[2 + 3 * i])
        ths[i] = float(toks[3 + 3 * i])
        ws[i] = float(toks[4 + 3 * i])
    cols = [[_zernike(j, ros[i], ths[i]) for j in range(1, jn + 1)] for i in range(n)]
    mat = [[0.0] * jn for _ in range(jn)]
    vec = [0.0] * jn
    for i in range(n):
        for a in range(jn):
            for b in range(jn):
                mat[a][b] += cols[i][a] * cols[i][b]
            vec[a] += cols[i][a] * ws[i]
    beta = _gauss_solve(mat, vec, jn)
    if beta is None:
        sys.stdout.write("SINGULAR")
        return
    ssres = 0.0
    ssdat = 0.0
    for i in range(n):
        pred = 0.0
        for a in range(jn):
            pred += beta[a] * cols[i][a]
        r = ws[i] - pred
        ssres += r * r
        ssdat += ws[i] * ws[i]
    rms = math.sqrt(ssres / n)
    rmsd = math.sqrt(ssdat / n)
    out = [
        "COEFFS " + " ".join(f"{_snap(b):.6f}" for b in beta),
        f"RMS {_snap(rms):.6f}",
        f"RMSDATA {_snap(rmsd):.6f}",
    ]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
