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
        n, g, m, r = (int(t) for t in toks[1:5])
        n2 = n * n
        sys.stdout.write(f"{_modexp(g, m, n2) * _modexp(r, n, n2) % n2}")
    elif toks[0] == "DEC":
        n, lam, mu, c = (int(t) for t in toks[1:5])
        n2 = n * n
        sys.stdout.write(f"{((_modexp(c, lam, n2) - 1) // n) * mu % n}")
    else:
        n, c1, c2 = (int(t) for t in toks[1:4])
        sys.stdout.write(f"{c1 * c2 % (n * n)}")


if __name__ == "__main__":
    main()
