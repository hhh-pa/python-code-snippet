"""Baum-Welch HMM training (AIMA 21.3.3, scaled forward-backward)."""

import sys


def _forward(pi, a, b, obs):
    s = len(pi)
    t = len(obs)
    al = [[0.0] * s for _ in range(t)]
    c = [0.0] * t
    for i in range(s):
        al[0][i] = pi[i] * b[i][obs[0]]
    c[0] = sum(al[0])
    for i in range(s):
        al[0][i] /= c[0]
    for tt in range(1, t):
        for j in range(s):
            tot = 0.0
            for i in range(s):
                tot += al[tt - 1][i] * a[i][j]
            al[tt][j] = b[j][obs[tt]] * tot
        c[tt] = sum(al[tt])
        for j in range(s):
            al[tt][j] /= c[tt]
    return al, c


def _backward(a, b, obs, c):
    s = len(a)
    t = len(obs)
    be = [[0.0] * s for _ in range(t)]
    for i in range(s):
        be[t - 1][i] = 1.0
    for tt in range(t - 2, -1, -1):
        for i in range(s):
            tot = 0.0
            for j in range(s):
                tot += a[i][j] * b[j][obs[tt + 1]] * be[tt + 1][j]
            be[tt][i] = tot / c[tt + 1]
    return be


def _gammas(al, be):
    s = len(al[0])
    gam = [[0.0] * s for _ in range(len(al))]
    for tt in range(len(al)):
        tot = 0.0
        for i in range(s):
            tot += al[tt][i] * be[tt][i]
        for i in range(s):
            gam[tt][i] = al[tt][i] * be[tt][i] / tot
    return gam


def _xis(al, be, a, b, obs):
    s = len(a)
    t = len(obs)
    xi = [[[0.0] * s for _ in range(s)] for _ in range(max(0, t - 1))]
    for tt in range(t - 1):
        tot = 0.0
        for i in range(s):
            for j in range(s):
                tot += al[tt][i] * a[i][j] * b[j][obs[tt + 1]] * be[tt + 1][j]
        for i in range(s):
            for j in range(s):
                xi[tt][i][j] = (
                    al[tt][i] * a[i][j] * b[j][obs[tt + 1]] * be[tt + 1][j] / tot
                )
    return xi


def _estep(pi, a, b, obs):
    al, c = _forward(pi, a, b, obs)
    be = _backward(a, b, obs, c)
    return _gammas(al, be), _xis(al, be, a, b, obs)


def _accumulate(s, o, acc, obs, gam, xi):
    pi_num, a_num, a_den, b_num, b_den = acc
    t = len(obs)
    for i in range(s):
        pi_num[i] += gam[0][i]
    for tt in range(t - 1):
        for i in range(s):
            a_den[i] += gam[tt][i]
            for j in range(s):
                a_num[i][j] += xi[tt][i][j]
    for tt in range(t):
        for j in range(s):
            b_den[j] += gam[tt][j]
            b_num[j][obs[tt]] += gam[tt][j]


def _mstep(s, o, pi, a, b, acc, nseq):
    pi_num, a_num, a_den, b_num, b_den = acc
    for i in range(s):
        pi[i] = pi_num[i] / nseq
        if a_den[i] > 0:
            for j in range(s):
                a[i][j] = a_num[i][j] / a_den[i]
        if b_den[i] > 0:
            for k in range(o):
                b[i][k] = b_num[i][k] / b_den[i]


def _run(s, pi, a, b, seqs, iters):
    o = len(b[0])
    for _ in range(iters):
        acc = (
            [0.0] * s,
            [[0.0] * s for _ in range(s)],
            [0.0] * s,
            [[0.0] * o for _ in range(s)],
            [0.0] * s,
        )
        for obs in seqs:
            gam, xi = _estep(pi, a, b, obs)
            _accumulate(s, o, acc, obs, gam, xi)
        _mstep(s, o, pi, a, b, acc, len(seqs))
    return pi, a, b


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    s, o, nl, n = int(toks[0]), int(toks[1]), int(toks[2]), int(toks[3])
    i = 4
    pi = list(map(float, toks[i : i + s]))
    i += s
    a = [list(map(float, toks[i + j * s : i + (j + 1) * s])) for j in range(s)]
    i += s * s
    b = [list(map(float, toks[i + j * o : i + (j + 1) * o])) for j in range(s)]
    i += s * o
    seqs = []
    for _ in range(nl):
        t = int(toks[i])
        seqs.append(list(map(int, toks[i + 1 : i + 1 + t])))
        i += 1 + t
    pi, a, b = _run(s, pi, a, b, seqs, n)
    out = [" ".join(f"{v:.6f}" for v in pi)]
    out += [" ".join(f"{v:.6f}" for v in row) for row in a]
    out += [" ".join(f"{v:.6f}" for v in row) for row in b]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
