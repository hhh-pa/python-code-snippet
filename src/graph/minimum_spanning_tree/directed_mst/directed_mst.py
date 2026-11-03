import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    root = int(next(it))

    es = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        es.append((u, v, w))

    INF = 4 * 10**18
    ans = 0

    while True:
        inw = [INF] * n
        pre = [-1] * n
        for u, v, w in es:
            if u != v and w < inw[v]:
                inw[v] = w
                pre[v] = u
        inw[root] = 0

        if any(x == INF for x in inw):
            print("NO ARBORESCENCE")
            return

        comp = [-1] * n
        vis = [-1] * n
        cn = 0

        for i in range(n):
            v = i
            while vis[v] != i and comp[v] == -1 and v != root:
                vis[v] = i
                v = pre[v]
            if v != root and comp[v] == -1:
                j = pre[v]
                while j != v:
                    comp[j] = cn
                    j = pre[j]
                comp[v] = cn
                cn += 1

        for x in inw:
            ans += x

        if cn == 0:
            break

        for i in range(n):
            if comp[i] == -1:
                comp[i] = cn
                cn += 1

        ne = []
        for u, v, w in es:
            if comp[u] != comp[v]:
                ne.append((comp[u], comp[v], w - inw[v]))

        root = comp[root]
        n = cn
        es = ne

    print(ans)

if __name__ == "__main__":
    main()
