"""Tree diameter in edges (two-pass farthest-node search)."""

import collections
import sys


def _bfs(adj, s):
    dist = [-1] * len(adj)
    dist[s] = 0
    dq = collections.deque([s])
    while dq:
        u = dq.popleft()
        for w in adj[u]:
            if dist[w] < 0:
                dist[w] = dist[u] + 1
                dq.append(w)
    return dist


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    adj = [[] for _ in range(n)]
    for i in range(n - 1):
        u, v = data[1 + 2 * i], data[2 + 2 * i]
        adj[u].append(v)
        adj[v].append(u)
    if n == 1:
        sys.stdout.write("0")
        return
    d0 = _bfs(adj, 0)
    a = max(range(n), key=lambda i: d0[i])
    sys.stdout.write(str(max(_bfs(adj, a))))


if __name__ == "__main__":
    main()
