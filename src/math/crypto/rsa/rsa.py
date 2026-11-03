import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    p = int(tokens[0])
    q = int(tokens[1])
    e = int(tokens[2])
    m = int(tokens[3])

    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    c = pow(m, e, n)

    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = pow(q, -1, p)
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = ((qinv * ((m1 - m2) % p)) % p + p) % p
    decrypted = m2 + h * q

    print(f"{n} {phi} {d}")
    print(c)
    print(decrypted)

if __name__ == '__main__':
    main()
