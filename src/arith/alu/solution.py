import sys


def _add_sub(a, b, sub):
    # Shared adder: SUB inverts B and sets carry-in (Fig 11.39/11.40).
    out = []
    carry = 1 if sub else 0
    for i in range(len(a)):
        bb = (1 - b[i]) if sub else b[i]
        bit = a[i] + bb + carry
        out.append(bit & 1)
        carry = bit >> 1
    return out, carry


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    op, a, b = toks[0], toks[1], toks[2]
    n = max(len(a), len(b))
    a = a.zfill(n)
    b = b.zfill(n)
    ab = [(ord(a[n - 1 - i]) - 48) for i in range(n)]
    # Mux-selected datapath.
    if op in ("ADD", "SUB"):
        bb = [(ord(b[n - 1 - i]) - 48) for i in range(n)]
        res, carry = _add_sub(ab, bb, op == "SUB")
    elif op in ("AND", "OR", "XOR"):
        bb = [(ord(b[n - 1 - i]) - 48) for i in range(n)]
        if op == "AND":
            res = [x & y for x, y in zip(ab, bb)]
        elif op == "OR":
            res = [x | y for x, y in zip(ab, bb)]
        else:
            res = [x ^ y for x, y in zip(ab, bb)]
        carry = 0
    else:
        k = int(b, 2)
        if op == "SHL":
            res = [0] * n
            for i in range(n):
                if i + k < n:
                    res[i + k] = ab[i]
        else:
            sign = ab[n - 1]
            res = [ab[i + k] if i + k < n else sign for i in range(n)]
        carry = 0
    zero = 1 if all(v == 0 for v in res) else 0
    neg = res[n - 1]
    sys.stdout.write("".join(chr(48 + res[i]) for i in range(n - 1, -1, -1)))
    sys.stdout.write(f" {carry}{zero}{neg}")


if __name__ == "__main__":
    main()
