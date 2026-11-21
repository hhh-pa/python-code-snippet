import sys


def _negate(bits):
    out = [1 - x for x in bits]
    carry = 1
    for i in range(len(out)):
        bit = out[i] + carry
        out[i] = bit & 1
        carry = bit >> 1
    return out


def _add(a, b):
    out = [0] * len(a)
    carry = 0
    for i in range(len(a)):
        bit = a[i] + b[i] + carry
        out[i] = bit & 1
        carry = bit >> 1
    return out


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    # Modified Booth radix-4 recoding (Table 11.2): overlapping 3-bit
    # groups of the multiplier select 0, +M, +2M, -M or -2M.
    m = [(ord(a[n - 1 - i]) - 48) for i in range(n)]
    y = [(ord(b[n - 1 - i]) - 48) for i in range(n)]
    width = 2 * n + 2
    acc = [0] * width
    # One zero bit above the MSB: recoding reads the top bit as a sign,
    # so unsigned operands need the extra group (out-of-range y = 0).
    groups = (n + 2) // 2
    for k in range(groups):
        b0 = y[2 * k - 1] if 2 * k - 1 >= 0 else 0
        b1 = y[2 * k] if 2 * k < n else 0
        b2 = y[2 * k + 1] if 2 * k + 1 < n else 0
        sel = (b2 << 2) | (b1 << 1) | b0
        if sel in (0, 7):
            continue
        pp = [0] * width
        off = 2 * k + 1 if sel in (3, 4) else 2 * k
        for i in range(n):
            pp[off + i] = m[i]
        if sel >= 4:
            pp = _negate(pp)
        acc = _add(acc, pp)
    sys.stdout.write("".join(chr(48 + acc[i]) for i in range(2 * n - 1, -1, -1)))


if __name__ == "__main__":
    main()
