import sys


def _breakpoints(p):
    n = len(p)
    bps = (1 if p[0] != 1 else 0) + (1 if p[-1] != n else 0)
    return bps + sum(1 for i in range(n - 1) if abs(p[i] - p[i + 1]) != 1)


def _strips(p):
    n = len(p)
    res, a = [], 0
    for i in range(n - 1):
        if abs(p[i] - p[i + 1]) != 1:
            res.append((a, i))
            a = i + 1
    res.append((a, n - 1))
    return res


def _decreasing(p, a, r):
    return a == r or all(p[i] > p[i + 1] for i in range(a, r))


def _step(p, n):
    dec = any(_decreasing(p, a, b) for a, b in _strips(p))
    cur = _breakpoints(p)
    for a in range(n):
        for b in range(a + 1, n):
            q = p[:a] + p[a : b + 1][::-1] + p[b + 1 :]
            bq = _breakpoints(q)
            if dec:
                ok = bq < cur
            else:
                ok = bq <= cur and any(_decreasing(q, x, y) for x, y in _strips(q))
            if ok:
                return q, (a + 1, b + 1)
    raise AssertionError("stuck")


def _step(p, n):
    dec = any(_decreasing(p, a, b) for a, b in _strips(p))
    cur = _breakpoints(p)
    for a in range(n):
        for b in range(a + 1, n):
            q = p[:a] + p[a : b + 1][::-1] + p[b + 1 :]
            bq = _breakpoints(q)
            if dec:
                ok = bq < cur
            else:
                ok = bq <= cur and any(_decreasing(q, x, y) for x, y in _strips(q))
            if ok:
                return q, (a + 1, b + 1)
    raise AssertionError("stuck")


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    p = [int(t) for t in toks[1:]]
    n = len(p)
    ops = []
    while _breakpoints(p) > 0:
        p, op = _step(p, n)
        ops.append(op)
    sys.stdout.write(" ".join([str(len(ops))] + [f"{a} {b}" for a, b in ops]))


if __name__ == "__main__":
    main()
