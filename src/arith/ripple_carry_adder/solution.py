import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    out = []
    carry = 0
    for i in range(n - 1, -1, -1):
        bit = (ord(a[i]) - 48) + (ord(b[i]) - 48) + carry
        out.append(chr(48 + (bit & 1)))
        carry = bit >> 1
    out.append(chr(48 + carry))
    sys.stdout.write("".join(reversed(out)))


if __name__ == "__main__":
    main()
