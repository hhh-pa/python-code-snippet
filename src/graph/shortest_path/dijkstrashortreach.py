import sys
import heapq

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
            w = int(next(it))
            adj[u].append((v, w))
            adj[v].append((u, w))

        s = int(next(it))

        dist = [-1] * (n + 1)
        dist[s] = 0
        pq = [(0, s)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if dist[v] == -1 or nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

        row = []
        for i in range(1, n + 1):
            if i != s:
                row.append(str(dist[i]))
        out.append(" ".join(row))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
