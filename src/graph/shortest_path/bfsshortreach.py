import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))

        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u = int(next(it))
            v = int(next(it))
            adj[u].append(v)
            adj[v].append(u)

        start = int(next(it))

        dist = [-1] * (n + 1)
        dist[start] = 0
        q = deque([start])

        while q:
            u = q.popleft()
            d_next = dist[u] + 6
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = d_next
                    q.append(v)

        row = []
        for i in range(1, n + 1):
            if i != start:
                row.append(str(dist[i]))
        out.append(" ".join(row))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
