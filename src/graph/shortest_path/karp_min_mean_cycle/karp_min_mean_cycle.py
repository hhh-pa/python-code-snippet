import sys
import math

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    es = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        es.append((u, v, w))

    INF = 4 * 10**18
    F = [[INF] * n for _ in range(n + 1)]
    for v in range(n):
        F[0][v] = 0

    for k in range(1, n + 1):
        F_prev = F[k - 1]
        F_curr = F[k]
        for u, v, w in es:
            val = F_prev[u] + w
            if val < F_curr[v]:
                F_curr[v] = val

    any_found = False
    bn = 0
    bd = 1

    for v in range(n):
        if F[n][v] >= INF // 2:
            continue
        av = False
        vn = 0
        vd = 1
        for k in range(n):
            if F[k][v] >= INF // 2:
                continue
            num = F[n][v] - F[k][v]
            den = n - k
            if not av or num * vd > vn * den:
                vn = num
                vd = den
                av = True
        if not av:
            continue
        if not any_found or vn * bd < bn * vd:
            bn = vn
            bd = vd
            any_found = True

    if not any_found:
        print("NO CYCLE")
        return

    g = math.gcd(bn, bd)
    print(f"{bn // g}/{bd // g}")

if __name__ == "__main__":
    main()
