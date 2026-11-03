import collections
import sys

def bfs_depth(adj, s):
    n = len(adj)
    if n == 0:
        return 0
    d = [-1] * n
    d[s] = 0
    q = collections.deque([s])
    mx = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                if d[v] > mx:
                    mx = d[v]
                q.append(v)
    return mx

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
    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))

    P = int(next(it))
    nc = int(next(it))
    cl = [int(next(it)) for _ in range(n)]

    cadj = [[] for _ in range(nc)]
    for _ in range(nc - 1):
        a = int(next(it))
        b = int(next(it))
        cadj[a].append(b)
        cadj[b].append(a)

    depth = bfs_depth(adj, 0)
    cdepth = bfs_depth(cadj, 0) if nc > 0 else 0

    minintra = 0
    for u, v in edges:
        if cl[u] == cl[v]:
            minintra += 1

    out = [
        f"ALPHA MESSAGES: {2 * m * P} TIME: {P}",
        f"BETA MESSAGES: {2 * (n - 1) * P} TIME: {2 * depth * P}",
        f"GAMMA MESSAGES: {(2 * minintra + 2 * (nc - 1)) * P} TIME: {(2 + 2 * cdepth) * P}",
    ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
