import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        adj[u].append((v, w))
        adj[v].append((u, w))

    start = int(next(it))

    pq = [(0, start)]
    in_mst = [False] * (n + 1)
    total_weight = 0

    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue
        in_mst[u] = True
        total_weight += w

        for v, weight in adj[u]:
            if not in_mst[v]:
                heapq.heappush(pq, (weight, v))

    print(total_weight)

if __name__ == "__main__":
    main()
