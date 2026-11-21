import sys


def _polymul(a, b, n, mod):
    c = [0] * n
    for i in range(n):
        for j in range(n):
            c[(i + j) % n] = (c[(i + j) % n] + a[i] * b[j]) % mod
    return c


def _center(v, mod):
    v %= mod
    return v - mod if v > mod // 2 else v


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 5:
        return
    n, p, q = (int(t) for t in toks[1:4])
    rest = [int(t) for t in toks[4:]]
    if toks[0] == "ENC":
        h, r, m = rest[:n], rest[n : 2 * n], rest[2 * n : 3 * n]
        e = [(a + b) % q for a, b in zip(_polymul(r, h, n, q), m)]
        sys.stdout.write(" ".join(str(_center(v, q)) for v in e))
    else:
        f, fp, e = rest[:n], rest[n : 2 * n], rest[2 * n : 3 * n]
        a = [
            _center(v, q)
            for v in _polymul([v % q for v in f], [v % q for v in e], n, q)
        ]
        sys.stdout.write(
            " ".join(str(v) for v in _polymul(fp, [v % p for v in a], n, p))
        )


if __name__ == "__main__":
    main()
