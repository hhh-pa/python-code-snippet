import sys
from collections import deque

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
    w = [[0] * n for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        res[u][v] += c
        res[v][u] += c
        w[u][v] += c
        w[v][u] += c

    flow = 0
    INF = 4 * 10**18
    while True:
        par = [-1] * n
        par[s] = s
        q = deque([s])
        while q and par[t] == -1:
            u = q.popleft()
            for v in range(n):
                if par[v] == -1 and res[u][v] > 0:
                    par[v] = u
                    q.append(v)
        if par[t] == -1:
            break
        b = INF
        v = t
        while v != s:
            p = par[v]
            if res[p][v] < b:
                b = res[p][v]
            v = p
        v = t
        while v != s:
            p = par[v]
            res[p][v] -= b
            res[v][p] += b
            v = p
        flow += b

    # Stoer-Wagner min cut
    alive = [True] * n
    best = float('inf')
    nn = n
    while nn > 1:
        added = [False] * n
        ws = [0] * n
        pre_last = -1
        last = -1
        for k in range(nn):
            sel = -1
            for v in range(n):
                if alive[v] and not added[v]:
                    if sel == -1 or ws[v] > ws[sel]:
                        sel = v
            added[sel] = True
            for v in range(n):
                if alive[v]:
                    ws[v] += w[sel][v]
            if k == nn - 2:
                pre_last = sel
            if k == nn - 1:
                last = sel
        coph = 0
        for v in range(n):
            if alive[v] and v != last:
                coph += w[last][v]
        if coph < best:
            best = coph
        for v in range(n):
            w[pre_last][v] += w[last][v]
            w[v][pre_last] += w[v][last]
        alive[last] = False
        nn -= 1

    print(flow)
    print(best)

if __name__ == "__main__":
    main()
