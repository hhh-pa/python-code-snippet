import sys
from collections import deque
import math

def dinic(N, cap, s, t):
    INF = 4 * 10**18
    flow = 0
    lvl = [-1] * N
    it = [0] * N

    def dfs(u, f):
        if u == t:
            return f
        for i in range(it[u], N):
            it[u] = i
            v = i
            if lvl[v] == lvl[u] + 1 and cap[u][v] > 0:
                r = dfs(v, min(f, cap[u][v]))
                if r:
                    cap[u][v] -= r
                    cap[v][u] += r
                    return r
        return 0

    while True:
        lvl = [-1] * N
        lvl[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in range(N):
                if lvl[v] == -1 and cap[u][v] > 0:
                    lvl[v] = lvl[u] + 1
                    q.append(v)
        if lvl[t] == -1:
            return flow
        it = [0] * N
        while True:
            r = dfs(s, INF)
            if not r:
                break
            flow += r

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    es = []
    deg = [0] * n
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        es.append((u, v))
        deg[u] += 1
        deg[v] += 1

    N = n + 2
    S = n
    T = n + 1

    cands = []
    for p in range(m + 1):
        for q in range(1, n + 1):
            cands.append((p, q))

    # Sort by p/q ascending, tie break by (p, q)
    from functools import cmp_to_key
    def cmp(a, b):
        l = a[0] * b[1]
        r = b[0] * a[1]
        if l != r:
            return -1 if l < r else 1
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0

    cands.sort(key=cmp_to_key(cmp))
    # Unique
    unique_cands = []
    for c in cands:
        if not unique_cands or cmp(unique_cands[-1], c) != 0:
            unique_cands.append(c)

    for p, q in unique_cands:
        cap = [[0] * N for _ in range(N)]
        for v in range(n):
            cap[S][v] += m * q
            cap[v][T] += m * q + 2 * p - q * deg[v]
        for u, v in es:
            cap[u][v] += q
            cap[v][u] += q
        if dinic(N, cap, S, T) == q * n * m:
            g = math.gcd(p, q)
            print(f"{p // g}/{q // g}")
            return

    print("0/1")

if __name__ == "__main__":
    main()
