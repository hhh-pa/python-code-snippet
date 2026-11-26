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
    if len(toks) < 5:
        return
    if toks[0] == "ENC":
        p, g, y, m, k = (int(t) for t in toks[1:6])
        c1 = _modexp(g, k, p)
        c2 = m * _modexp(y, k, p) % p
        sys.stdout.write(f"{c1} {c2}")
    else:
        p, x, c1, c2 = (int(t) for t in toks[1:5])
        sys.stdout.write(f"{c2 * _modexp(c1, p - 1 - x, p) % p}")


if __name__ == "__main__":
    main()
