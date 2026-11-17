import sys


def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def _modinv(a, m):
    return _egcd(a, m)[1] % m


def _tonelli(a, p):
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        t2, i = (t * t) % p, 1
        while t2 != 1:
            t2 = (t2 * t2) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def _hensel(a, p, e, r0):
    r, m = r0, p
    for _ in range(1, e):
        m *= p
        fr = (r * r - a) % m
        r = (r - fr * _modinv((2 * r) % m, m)) % m
    return r


def _prime_power_root(a, p, e):
    n = p**e
    a %= n
    if a % p == 0:
        va, t = 0, a
        while t % p == 0 and t:
            t //= p
            va += 1
        if a == 0:
            return 0
        if va % 2 == 1:
            return -1
        sub = _prime_power_root(t, p, e - va)
        if sub == -1:
            return -1
        r = (sub * p ** (va // 2)) % n
        return min(r, n - r)
    r0 = _tonelli(a, p)
    if r0 is None:
        return -1
    r = _hensel(a, p, e, r0)
    return min(r, n - r)


def _factorize(n):
    facs = {}
    v, d = n, 2
    while d * d <= v:
        while v % d == 0:
            facs[d] = facs.get(d, 0) + 1
            v //= d
        d += 1 if d == 2 else 2
    if v > 1:
        facs[v] = facs.get(v, 0) + 1
    return facs


def _semiprime_root(a, n, p, q):
    rp = _tonelli(a, p)
    rq = _tonelli(a, q)
    if rp is None or rq is None:
        return -1
    best = None
    for sp in (rp, (-rp) % p):
        for sq in (rq, (-rq) % q):
            r = (sp + p * (((sq - sp) * _modinv(p % q, q)) % q)) % n
            if best is None or r < best:
                best = r
    return best


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, n = int(toks[0]), int(toks[1])
    facs = _factorize(n)
    if len(facs) == 1:
        p, e = next(iter(facs.items()))
        sys.stdout.write(str(_prime_power_root(a, p, e)))
    elif len(facs) == 2 and all(e == 1 for e in facs.values()):
        p, q = sorted(facs)
        sys.stdout.write(str(_semiprime_root(a, n, p, q)))
    else:
        sys.stdout.write("-1")


if __name__ == "__main__":
    main()
