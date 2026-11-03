import sys
from collections import deque

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    e = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(e):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)

    pair_u = [0] * (n + 1)
    pair_v = [0] * (m + 1)
    dist = [0] * (n + 1)
    INF = 10**9

    def bfs():
        q = deque()
        for u in range(1, n + 1):
            if pair_u[u] == 0:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        dist[0] = INF

        while q:
            u = q.popleft()
            if dist[u] < dist[0]:
                for v in adj[u]:
                    next_u = pair_v[v]
                    if dist[next_u] == INF:
                        dist[next_u] = dist[u] + 1
                        q.append(next_u)
        return dist[0] != INF

    def dfs(u):
        if u != 0:
            for v in adj[u]:
                next_u = pair_v[v]
                if dist[next_u] == dist[u] + 1:
                    if dfs(next_u):
                        pair_v[v] = u
                        pair_u[u] = v
                        return True
            dist[u] = INF
            return False
        return True

    matching = 0
    while bfs():
        for u in range(1, n + 1):
            if pair_u[u] == 0 and dfs(u):
                matching += 1

    out = [str(matching)]
    for u in range(1, n + 1):
        if pair_u[u] != 0:
            out.append(f"{u} {pair_u[u]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
