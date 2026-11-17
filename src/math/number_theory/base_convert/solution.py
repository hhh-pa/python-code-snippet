import sys

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    sb, db, dg = int(toks[0]), int(toks[1]), toks[2].strip().upper()
    # Repeated divmod on the digit array (base sb), collecting remainders.
    cur = [DIGITS.index(c) for c in dg]
    if not cur or all(d == 0 for d in cur):
        sys.stdout.write("0")
        return
    out = []
    while cur:
        nxt = []
        carry = 0
        for d in cur:
            v = carry * sb + d
            q, carry = v // db, v % db
            if nxt or q:
                nxt.append(q)
        out.append(DIGITS[carry])
        cur = nxt
    sys.stdout.write("".join(reversed(out)))


if __name__ == "__main__":
    main()
