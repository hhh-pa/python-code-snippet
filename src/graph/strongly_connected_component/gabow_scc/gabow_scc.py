import sys
from collections import defaultdict

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)

    pre = [0] * n
    comp = [-1] * n
    S = []
    P = []
    C = 0

    def dfs(v):
        nonlocal C
        C += 1
        pre[v] = C
        S.append(v)
        P.append(v)

        for w in adj[v]:
            if pre[w] == 0:
                dfs(w)
            elif comp[w] == -1:
                while pre[P[-1]] > pre[w]:
                    P.pop()

        if P[-1] == v:
            P.pop()
            while True:
                x = S.pop()
                comp[x] = v
                if x == v:
                    break

    for v in range(n):
        if pre[v] == 0:
            dfs(v)

    g = defaultdict(list)
    for v in range(n):
        g[comp[v]].append(v)

    lab = [0] * n
    for vs in g.values():
        mn = min(vs)
        for v in vs:
            lab[v] = mn

    print(len(g))
    print(" ".join(str(x) for x in lab))

if __name__ == "__main__":
    main()
