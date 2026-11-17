import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    g = [(ord(a[n - 1 - i]) - 48) & (ord(b[n - 1 - i]) - 48) for i in range(n)]
    p = [(ord(a[n - 1 - i]) - 48) ^ (ord(b[n - 1 - i]) - 48) for i in range(n)]
    stride = 1
    while stride < n:
        go, po = list(g), list(p)
        for i in range(stride, n):
            g[i] = go[i] | (po[i] & go[i - stride])
            p[i] = po[i] & po[i - stride]
        stride *= 2
    out = [str(g[n - 1])]
    for i in range(n - 1, -1, -1):
        x = ord(a[n - 1 - i]) - 48
        y = ord(b[n - 1 - i]) - 48
        carry = 0 if i == 0 else g[i - 1]
        out.append(str(x ^ y ^ carry))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
