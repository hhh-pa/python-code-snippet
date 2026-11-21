import sys


def _modexp(b, e, m):
    r = 1 % m
    b %= m
    while e:
        if e & 1:
            r = r * b % m
        b = b * b % m
        e >>= 1
    return r


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 4:
        return
    if toks[0] == "ENC":
        n, x = int(toks[1]), int(toks[2])
        bits = toks[3]
        rs = [int(t) for t in toks[4:]]
        out = []
        for b, r in zip(bits, rs):
            out.append(str(r * r * (x if b == "1" else 1) % n))
        sys.stdout.write(" ".join(out))
    else:
        p = int(toks[1])
        cs = [int(t) for t in toks[3:]]
        sys.stdout.write(
            "".join("1" if _modexp(c, (p - 1) // 2, p) == p - 1 else "0" for c in cs)
        )


if __name__ == "__main__":
    main()
