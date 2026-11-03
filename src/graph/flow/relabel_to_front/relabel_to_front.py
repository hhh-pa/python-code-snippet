import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))
    t = int(next(it))

    res = [[0] * n for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        res[u][v] += c

    h = [0] * n
    e = [0] * n
    h[s] = n

    for v in range(n):
        if res[s][v] > 0:
            c = res[s][v]
            e[v] = c
            e[s] -= c
            res[v][s] += c
            res[s][v] = 0

    L = [v for v in range(n) if v != s and v != t]
    cur = [0] * n
    p = 0
    INF = 10**18

    while p < len(L):
        u = L[p]
        old = h[u]
        while e[u] > 0:
            v = cur[u]
            if v == n:
                mn = INF
                for w in range(n):
                    if res[u][w] > 0:
                        if h[w] < mn:
                            mn = h[w]
                h[u] = mn + 1
                cur[u] = 0
            elif res[u][v] > 0 and h[u] == h[v] + 1:
                d = min(e[u], res[u][v])
                res[u][v] -= d
                res[v][u] += d
                e[u] -= d
                e[v] += d
            else:
                cur[u] += 1

        if h[u] > old:
            u_val = L.pop(p)
            L.insert(0, u_val)
            p = 0
        else:
            p += 1

    print(e[t])

if __name__ == "__main__":
    main()
