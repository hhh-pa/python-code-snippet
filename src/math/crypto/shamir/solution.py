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


def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def _modinv(a, m):
    return _egcd(a % m, m)[1] % m


def _eval(coeffs, x, prime):
    y = 0
    for c in reversed(coeffs):
        y = (y * x + c) % prime
    return y


def _combine(shares, prime):
    s = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i == j:
                continue
            num = num * (-xj) % prime
            den = den * (xi - xj) % prime
        s = (s + yi * num * _modinv(den, prime)) % prime
    return s


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    if toks[0] == "SPLIT":
        prime, secret, n, _t = (int(x) for x in toks[1:5])
        coeffs = [secret] + [int(x) for x in toks[5:]]
        out = []
        for xx in range(1, n + 1):
            out += [str(xx), str(_eval(coeffs, xx, prime))]
        sys.stdout.write(" ".join(out))
    else:
        prime = int(toks[1])
        vals = [int(x) for x in toks[2:]]
        shares = [(vals[i], vals[i + 1]) for i in range(0, len(vals), 2)]
        sys.stdout.write(f"{_combine(shares, prime)}")


if __name__ == "__main__":
    main()
