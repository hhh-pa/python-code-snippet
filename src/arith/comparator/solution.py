import sys


def _subtract(a, b):
    # Two's-complement subtractor: invert B, add with carry-in 1.
    # Returns (difference_bits_lsb_first, carry_out).
    diff = []
    carry = 1
    for i in range(len(a)):
        bit = a[i] + (1 - b[i]) + carry
        diff.append(bit & 1)
        carry = bit >> 1
    return diff, carry


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, b = toks[0], toks[1]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    ab = [(ord(a[n - 1 - i]) - 48) for i in range(n)]
    bb = [(ord(b[n - 1 - i]) - 48) for i in range(n)]
    diff, carry_out = _subtract(ab, bb)
    ge = carry_out
    eq = 1 if all(d == 0 for d in diff) else 0
    _, carry_swapped = _subtract(bb, ab)
    le = carry_swapped
    sys.stdout.write(f"{ge}{eq}{le}")


if __name__ == "__main__":
    main()
