import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a = int(tokens[0])
    p = int(tokens[1])

    a = ((a % p) + p) % p
    if a == 0:
        print(0)
        return
    if p == 2:
        print(a)
        return

    # Check legendre symbol
    if pow(a, (p - 1) // 2, p) != 1:
        print("NONE")
        return

    q = p - 1
    s = 0
    while (q & 1) == 0:
        q >>= 1
        s += 1

    if s == 1:
        r = pow(a, (p + 1) // 4, p)
        print(min(r, p - r))
        return

    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s

    while t != 1:
        t2 = t
        i = 1
        while i < m:
            t2 = (t2 * t2) % p
            if t2 == 1:
                break
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i

    print(min(r, p - r))

if __name__ == '__main__':
    main()
