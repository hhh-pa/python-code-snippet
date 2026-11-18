"""Pearson + Spearman correlation (Think Stats 2e ch 7)."""

import math
import sys


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


def _midranks(xs):
    n = len(xs)
    order = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j + 2) / 2
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    xs = [0] * n
    ys = [0] * n
    for i in range(n):
        xs[i] = int(toks[1 + 2 * i])
        ys[i] = int(toks[2 + 2 * i])
    r = _pearson(xs, ys)
    rho = _pearson(_midranks(xs), _midranks(ys))
    sys.stdout.write(f"PEARSON {r:.6f}\nSPEARMAN {rho:.6f}")


if __name__ == "__main__":
    main()
