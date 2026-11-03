import sys

MOD = 998244353
G = 3

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[1 + i]) % MOD for i in range(n)]

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
        for i in range(0, n, length):
            w = 1
            for j in range(half):
                u = a[i + j]
                v = (a[i + j + half] * w) % MOD
                a[i + j] = (u + v) % MOD
                a[i + j + half] = (u - v + MOD) % MOD
                w = (w * wlen) % MOD
        length <<= 1

    print(*(a))

if __name__ == '__main__':
    main()
