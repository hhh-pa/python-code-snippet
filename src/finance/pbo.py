"""Probability of backtest overfitting (AFML ch 11)."""

import itertools
import math
import sys


def _sharpe(vals):
    n = len(vals)
    if n < 2:
        return 0.0
    mean = sum(vals) / n
    var = sum((x - mean) * (x - mean) for x in vals) / (n - 1)
    std = math.sqrt(var)
    if std == 0.0:
        return 0.0
    return mean / std


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
    t = int(toks[0])
    n = int(toks[1])
    s = int(toks[2])
    mat = []
    idx = 3
    for _ in range(t):
        mat.append(list(map(float, toks[idx : idx + n])))
        idx += n
    q, rem = divmod(t, s)
    bounds = [0]
    for g in range(s):
        bounds.append(bounds[-1] + q + (1 if g < rem else 0))
    bad = 0
    total = 0
    for combo in itertools.combinations(range(s), s // 2):
        inset = set(combo)
        is_rows = []
        oos_rows = []
        for g in range(s):
            target = is_rows if g in inset else oos_rows
            target.extend(range(bounds[g], bounds[g + 1]))
        is_sh = [_sharpe([mat[r][c] for r in is_rows]) for c in range(n)]
        oos_sh = [_sharpe([mat[r][c] for r in oos_rows]) for c in range(n)]
        is_rk = _midranks(is_sh)
        oos_rk = _midranks(oos_sh)
        med = (n + 1) / 2
        sel = [oos_rk[c] for c in range(n) if is_rk[c] > med]
        w = 0.5 if not sel else sum(sel) / len(sel) / (n + 1)
        if w < 0.5:
            bad += 1
        total += 1
    sys.stdout.write(f"PBO {bad / total:.6f}")


if __name__ == "__main__":
    main()
