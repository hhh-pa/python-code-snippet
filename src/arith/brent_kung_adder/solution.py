import sys


def op(a, b):
    (g, p), (g2, p2) = a, b
    return (1 if g == 1 or (p == 1 and g2 == 1) else 0, 1 if p == 1 and p2 == 1 else 0)


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    size = 1
    while size < n:
        size *= 2
    gp = []
    for i in range(size):
        if i < n:
            x = ord(a[n - 1 - i]) - 48
            y = ord(b[n - 1 - i]) - 48
            gp.append((x & y, x ^ y))
        else:
            gp.append((0, 1))
    orig = list(gp)
    stride = 1
    while stride < size:
        for i in range(2 * stride - 1, size, 2 * stride):
            gp[i] = op(gp[i], gp[i - stride])
        stride *= 2
    gp[size - 1] = (0, 1)
    stride = size // 2
    while stride >= 1:
        for i in range(2 * stride - 1, size, 2 * stride):
            t = gp[i - stride]
            gp[i - stride] = gp[i]
            gp[i] = op(gp[i], t)
        stride //= 2
    out = []
    g0, p0 = orig[n - 1]
    out.append(str(1 if g0 == 1 or (p0 == 1 and gp[n - 1][0] == 1) else 0))
    for i in range(n - 1, -1, -1):
        x = ord(a[n - 1 - i]) - 48
        y = ord(b[n - 1 - i]) - 48
        out.append(str(x ^ y ^ gp[i][0]))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
