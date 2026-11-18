"""Permutation tests (Think Stats 2e ch 9)."""

import math
import sys

MOD = 1 << 31


def _pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    c = 0.0
    vx = 0.0
    vy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        c += dx * dy
        vx += dx * dx
        vy += dy * dy
    if vx == 0.0 or vy == 0.0:
        return 0.0
    return c / math.sqrt(vx * vy)


def _draw(rng, u):
    rng[0] = (1103515245 * rng[0] + 12345) % MOD
    return rng[0] % u


def _shuffle(pool, rng):
    a = list(pool)
    for i in range(len(a) - 1, 0, -1):
        j = _draw(rng, i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def _read_groups(toks):
    n1 = int(toks[1])
    g1 = list(map(int, toks[2 : 2 + n1]))
    n2 = int(toks[2 + n1])
    g2 = list(map(int, toks[3 + n1 : 3 + n1 + n2]))
    k = int(toks[3 + n1 + n2])
    seed = int(toks[4 + n1 + n2])
    return n1, g1, n2, g2, k, seed


def _run_diff(toks):
    n1, g1, n2, g2, k, seed = _read_groups(toks)
    rng = [seed]
    obs = sum(g1) / n1 - sum(g2) / n2
    nobs = abs(sum(g1) * n2 - sum(g2) * n1)
    pool = g1 + g2
    cnt = 0
    for _ in range(k):
        a = _shuffle(pool, rng)
        s1 = sum(a[:n1])
        s2 = sum(a[n1:])
        if abs(s1 * n2 - s2 * n1) >= nobs:
            cnt += 1
    return obs, cnt, k


def _run_corr(toks):
    n = int(toks[1])
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(toks[2 + 2 * i])
        ys[i] = int(toks[3 + 2 * i])
    k = int(toks[2 + 2 * n])
    rng = [int(toks[3 + 2 * n])]
    obs = _pearson(xs, ys)
    arobs = abs(obs)
    cnt = 0
    for _ in range(k):
        if abs(_pearson(xs, _shuffle(ys, rng))) >= arobs:
            cnt += 1
    return obs, cnt, k


def _run_prop(toks):
    n1, g1, n2, g2, k, seed = _read_groups(toks)
    rng = [seed]
    c1 = sum(1 for v in g1 if v == 1)
    c2 = sum(1 for v in g2 if v == 1)
    obs = c1 / n1 - c2 / n2
    nobs = abs(c1 * n2 - c2 * n1)
    pool = g1 + g2
    cnt = 0
    for _ in range(k):
        a = _shuffle(pool, rng)
        d1 = sum(1 for v in a[:n1] if v == 1)
        d2 = sum(1 for v in a[n1:] if v == 1)
        if abs(d1 * n2 - d2 * n1) >= nobs:
            cnt += 1
    return obs, cnt, k


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    mode = toks[0]
    if mode == "DIFF":
        obs, cnt, k = _run_diff(toks)
    elif mode == "CORR":
        obs, cnt, k = _run_corr(toks)
    else:
        obs, cnt, k = _run_prop(toks)
    sys.stdout.write(f"OBS {obs:.6f}\nP {cnt / k:.6f}")


if __name__ == "__main__":
    main()
