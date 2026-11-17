import sys


def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def _modinv(a, m):
    return _egcd(a, m)[1] % m


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    p, g, h = int(toks[0]), int(toks[1]), int(toks[2])
    n = p - 1
    # Trial-factor p-1 into prime powers.
    facs = {}
    v, d = n, 2
    while d * d <= v:
        while v % d == 0:
            facs[d] = facs.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    if v > 1:
        facs[v] = facs.get(v, 0) + 1
    # DLOG per prime power, then CRT.
    congs = []
    for q, e in facs.items():
        qe = q**e
        gi = pow(g, n // qe, p)
        hi = pow(h, n // qe, p)
        gamma = pow(gi, q ** (e - 1), p)
        table = {}
        cur = 1
        for j in range(q):
            table[cur] = j
            cur = cur * gamma % p
        xi, hcur = 0, hi
        for k in range(e):
            hk = pow(hcur, q ** (e - 1 - k), p)
            dk = table[hk]
            xi += dk * (q**k)
            hcur = hcur * pow(gi, p - 1 - (dk * (q**k) % (p - 1)), p) % p
        congs.append((xi, qe))
    x, m = 0, 1
    for xi, mi in congs:
        inv = _modinv(m % mi, mi)
        x = (x + m * (((xi - x) * inv) % mi)) % (m * mi)
        m *= mi
    sys.stdout.write(str(x % n))


if __name__ == "__main__":
    main()
