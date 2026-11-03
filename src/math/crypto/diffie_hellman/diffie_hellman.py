import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    p = int(tokens[0])
    g = int(tokens[1])
    a = int(tokens[2])
    b = int(tokens[3])
    m = int(tokens[4])
    r = int(tokens[5])

    A = pow(g, a, p)
    B = pow(g, b, p)
    s = pow(B, a, p)

    c1 = pow(g, r, p)
    c2 = (m * pow(B, r, p)) % p

    shared_secret = pow(c1, b, p)
    inv_s = pow(shared_secret, -1, p)
    dm = (c2 * inv_s) % p

    print(f"{A} {B} {s}")
    print(f"{c1} {c2}")
    print(dm)

if __name__ == '__main__':
    main()
