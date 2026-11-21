import sys


def _greedy(a, b):
    n, m = len(a), len(b)
    trace = []
    v = {1: 0}
    found = None
    for d in range(n + m + 1):
        cur = {}
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            cur[k] = x
            if x >= n and y >= m:
                found = d
                break
        trace.append(dict(v))
        v = cur
        if found is not None:
            break
    return found, trace, n, m


def _traceback(a, b, trace, found):
    n, m = len(a), len(b)
    ops = []
    x, y = n, m
    for d in range(found, 0, -1):
        v = trace[d]
        k = x - y
        if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
            prev_x = v[k + 1]
            while x > prev_x:
                ops.append("=")
                x -= 1
                y -= 1
            ops.append("+")
            y -= 1
        else:
            prev_x = v[k - 1]
            while x > prev_x + 1:
                ops.append("=")
                x -= 1
                y -= 1
            ops.append("-")
            x -= 1
    while x > 0 and y > 0:
        ops.append("=")
        x -= 1
        y -= 1
    ops.reverse()
    return found, "".join(ops)


def main():
    toks = sys.stdin.read().strip().split(" ")
    if len(toks) < 2:
        return
    a = toks[1] if len(toks) > 1 else ""
    b = toks[2] if len(toks) > 2 else ""
    found, trace, _, _ = _greedy(a, b)
    dist, ops = _traceback(a, b, trace, found)
    sys.stdout.write(f"{dist}\n{ops}")


if __name__ == "__main__":
    main()
