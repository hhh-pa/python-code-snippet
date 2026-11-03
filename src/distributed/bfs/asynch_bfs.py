import sys

INF = 1000000000

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    root = int(next(it))
    dist = [INF] * n
    parent = [-1] * n
    vis = [False] * n

    vis[root] = True
    dist[root] = 0
    frontier = [root]
    d = 0

    while frontier:
        nf = []
        for u in frontier:
            dist[u] = d
            for v in adj[u]:
                if not vis[v]:
                    vis[v] = True
                    parent[v] = u
                    nf.append(v)
        frontier = nf
        d += 1

    msgs = 0
    for u in range(n):
        if vis[u]:
            for v in adj[u]:
                if u < v or not vis[v]:
                    msgs += 1
    msgs *= 2

    out = []
    for i in range(n):
        out.append(f"{i} {parent[i]} {-1 if dist[i] == INF else dist[i]}")
    out.append(f"MESSAGES: {msgs}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
