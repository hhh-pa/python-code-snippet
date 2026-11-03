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
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        res[u][v] += c

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

    print(flow)

if __name__ == "__main__":
    main()
