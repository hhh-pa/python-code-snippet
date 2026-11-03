import sys

def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = ext_gcd(b, a % b)
    return d, y1, x1 - y1 * (a // b)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    k = int(tokens[0])
    idx = 1
    r = []
    m = []
    for _ in range(k):
        r.append(int(tokens[idx]))
        m.append(int(tokens[idx + 1]))
        idx += 2

    r1 = r[0]
    m1 = m[0]
    ok = True

    for i in range(1, k):
        r2 = r[i]
        m2 = m[i]

        g, p, _ = ext_gcd(m1, m2)
        if (r2 - r1) % g != 0:
            ok = False
            break

        m2_reduced = m2 // g
        factor = ((r2 - r1) // g) % m2_reduced
        k1 = (p % m2_reduced * factor) % m2_reduced
        if k1 < 0:
            k1 += m2_reduced

        new_m = m1 * m2_reduced
        new_r = (r1 + m1 * k1) % new_m
        if new_r < 0:
            new_r += new_m

        r1 = new_r
        m1 = new_m

    if ok:
        print(f"{r1} {m1}")
    else:
        print("NO SOLUTION")

if __name__ == '__main__':
    main()
