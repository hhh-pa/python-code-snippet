import sys

MOD = 998244353
G = 3

def ntt(a, invert):
    n = len(a)
    # Bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        half = length >> 1
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            for j in range(half):
                u = a[i + j]
                v = (a[i + j + half] * w) % MOD
                a[i + j] = (u + v) % MOD
                a[i + j + half] = (u - v + MOD) % MOD
                w = (w * wlen) % MOD
        length <<= 1

    if invert:
        n_inv = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = (a[i] * n_inv) % MOD

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    deg_a = int(tokens[0])
    deg_b = int(tokens[1])
    idx = 2
    a = [int(tokens[idx + i]) for i in range(deg_a + 1)]
    idx += deg_a + 1
    b = [int(tokens[idx + i]) for i in range(deg_b + 1)]
    idx += deg_b + 1

    n = 1
    while n < deg_a + deg_b + 1:
        n <<= 1

    a.extend([0] * (n - len(a)))
    b.extend([0] * (n - len(b)))

    ntt(a, False)
    ntt(b, False)

    for i in range(n):
        a[i] = (a[i] * b[i]) % MOD

    ntt(a, True)

    final_deg = deg_a + deg_b
    print(final_deg)
    print(*(a[: final_deg + 1]))

if __name__ == '__main__':
    main()
