import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    # One partial product per multiplier bit, accumulated row by row
    # with ripple-carry addition (array structure, shift by wiring).
    acc = [0] * (2 * n)
    for j in range(n):
        if b[n - 1 - j] == "1":
            carry = 0
            for i in range(n):
                bit = acc[i + j] + (ord(a[n - 1 - i]) - 48) + carry
                acc[i + j] = bit & 1
                carry = bit >> 1
            pos = n + j
            while carry:
                bit = acc[pos] + carry
                acc[pos] = bit & 1
                carry = bit >> 1
                pos += 1
    sys.stdout.write("".join(chr(48 + acc[i]) for i in range(2 * n - 1, -1, -1)))


if __name__ == "__main__":
    main()
