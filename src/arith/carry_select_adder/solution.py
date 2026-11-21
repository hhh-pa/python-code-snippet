import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    out = ["0"] * (n + 1)
    carry = 0
    base = 0
    while base < n:
        w = min(4, n - base)
        both = []
        for cin in (0, 1):
            s = ["0"] * w
            c = cin
            for j in range(w):
                x = ord(a[n - 1 - (base + j)]) - 48
                y = ord(b[n - 1 - (base + j)]) - 48
                bit = x + y + c
                s[w - 1 - j] = chr(48 + (bit & 1))
                c = bit >> 1
            both.append(("".join(s), c))
        sel, carry = both[carry]
        for j in range(w):
            out[n - base - w + 1 + j] = sel[j]
        base += 4
    out[0] = chr(48 + carry)
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
