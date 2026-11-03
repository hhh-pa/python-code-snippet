import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    g = int(tokens[0])
    h = int(tokens[1])
    p = int(tokens[2])

    g = ((g % p) + p) % p
    h = ((h % p) + p) % p
    if h == 1:
        print(0)
        return

    m = math.isqrt(p)
    if m * m < p:
        m += 1

    table = {}
    cur = 1
    for j in range(m):
        if cur not in table:
            table[cur] = j
        cur = (cur * g) % p

    gm = pow(g, m, p)
    # Compute modular inverse of gm mod p via pow(gm, -1, p)
    try:
        factor = pow(gm, -1, p)
    except ValueError:
        factor = 1

    gamma = h
    for i in range(m):
        if gamma in table:
            ans = i * m + table[gamma]
            if pow(g, ans, p) == h:
                print(ans)
                return
        gamma = (gamma * factor) % p

    print("NONE")

if __name__ == '__main__':
    main()
