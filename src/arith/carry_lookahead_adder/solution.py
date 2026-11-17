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
    c = [0] * (n + 1)
    for i in range(n):
        carry = g[i]
        prod = 1
        for j in range(i, 0, -1):
            prod = prod & p[j]
            if prod == 1 and g[j - 1] == 1:
                carry = 1
                break
        c[i + 1] = carry
    out = [str(c[n])]
    for i in range(n - 1, -1, -1):
        x = ord(a[n - 1 - i]) - 48
        y = ord(b[n - 1 - i]) - 48
        out.append(str(x ^ y ^ c[i]))
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
