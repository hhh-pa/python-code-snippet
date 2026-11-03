import sys

MOD = 1000000007

def mod_norm(x):
    r = x % MOD
    return r if r >= 0 else r + MOD

def karatsuba(a, b):
    n = len(a)
    m = len(b)
    if n == 0 or m == 0:
        return []
    if min(n, m) <= 32:
        c = [0] * (n + m - 1)
        for i in range(n):
            ai = a[i]
            for j in range(m):
                c[i + j] = (c[i + j] + ai * b[j]) % MOD
        return c

    k = max(n, m) // 2
    a0 = a[: min(k, n)]
    a1 = a[k:] if n > k else []
    b0 = b[: min(k, m)]
    b1 = b[k:] if m > k else []

    z0 = karatsuba(a0, b0)
    z2 = karatsuba(a1, b1)

    asz = max(len(a0), len(a1))
    bsz = max(len(b0), len(b1))
    asum = [0] * asz
    bsum = [0] * bsz

    for i in range(len(a0)):
        asum[i] = (asum[i] + a0[i]) % MOD
    for i in range(len(a1)):
        asum[i] = (asum[i] + a1[i]) % MOD
    for i in range(len(b0)):
        bsum[i] = (bsum[i] + b0[i]) % MOD
    for i in range(len(b1)):
        bsum[i] = (bsum[i] + b1[i]) % MOD

    z1 = karatsuba(asum, bsum)

    # z1 = z1 - z0 - z2
    target_len = max(len(z1), max(len(z0), len(z2)))
    if len(z1) < target_len:
        z1.extend([0] * (target_len - len(z1)))

    for i in range(len(z0)):
        z1[i] = (z1[i] - z0[i]) % MOD
    for i in range(len(z2)):
        z1[i] = (z1[i] - z2[i]) % MOD

    res = [0] * (n + m - 1)
    for i in range(len(z0)):
        res[i] = (res[i] + z0[i]) % MOD
    for i in range(len(z1)):
        res[i + k] = (res[i + k] + z1[i]) % MOD
    for i in range(len(z2)):
        res[i + 2 * k] = (res[i + 2 * k] + z2[i]) % MOD

    return res

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    da = int(tokens[0])
    db = int(tokens[1])
    idx = 2
    a = [mod_norm(int(tokens[idx + i])) for i in range(da + 1)]
    idx += da + 1
    b = [mod_norm(int(tokens[idx + i])) for i in range(db + 1)]
    idx += db + 1

    c = karatsuba(a, b)
    dc = da + db
    print(dc)
    print(*(c[: dc + 1]))

if __name__ == '__main__':
    main()
