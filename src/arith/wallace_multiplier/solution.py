import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    # AND partial-product matrix, one row per multiplier bit.
    width = 2 * n + 2
    cols = [[] for _ in range(width)]
    for j in range(n):
        if b[n - 1 - j] == "1":
            for i in range(n):
                cols[i + j].append(ord(a[n - 1 - i]) - 48)
    # Staged 3:2 / 2:2 reduction until every column holds <= 2 bits.
    while max(len(c) for c in cols) > 2:
        nxt = [[] for _ in range(width)]
        for c in range(width - 1):
            bits = cols[c]
            k = 0
            while k + 3 <= len(bits):
                x, y, z = bits[k], bits[k + 1], bits[k + 2]
                nxt[c].append(x ^ y ^ z)
                nxt[c + 1].append((x + y + z) >> 1)
                k += 3
            nxt[c].extend(bits[k:])
        # Columns >= 2n stay empty (value conservation: 3 bits at
        # column 2n-1 already exceed any 2n-bit product), but pass the
        # last column through rather than dropping it silently.
        nxt[width - 1].extend(cols[width - 1])
        cols = nxt
    # Final carry-propagating addition of the two rows.
    out = []
    carry = 0
    for c in range(2 * n):
        bit = carry + (cols[c][0] if len(cols[c]) > 0 else 0)
        if len(cols[c]) > 1:
            bit += cols[c][1]
        out.append(chr(48 + (bit & 1)))
        carry = bit >> 1
    sys.stdout.write("".join(reversed(out)))


if __name__ == "__main__":
    main()
