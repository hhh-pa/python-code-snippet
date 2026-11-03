import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))

    adj = [[] for _ in range(n)]
    ind = [0] * n
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        adj[u].append((v, w))
        ind[v] += 1

    h = [i for i in range(n) if ind[i] == 0]
    heapq.heapify(h)
    topo = []
    while h:
        u = heapq.heappop(h)
        topo.append(u)
        for v, w in adj[u]:
            ind[v] -= 1
            if ind[v] == 0:
                heapq.heappush(h, v)

    INF = 4 * 10**18
    ds = [INF] * n
    dl = [-INF] * n
    ds[s] = 0
    dl[s] = 0

    for u in topo:
        for v, w in adj[u]:
            if ds[u] + w < ds[v]:
                ds[v] = ds[u] + w
            if dl[u] > -INF // 2 and dl[u] + w > dl[v]:
                dl[v] = dl[u] + w

    row1 = [("INF" if ds[i] >= INF // 2 else str(ds[i])) for i in range(n)]
    row2 = [("-INF" if dl[i] <= -INF // 2 else str(dl[i])) for i in range(n)]
    print(" ".join(row1))
    print(" ".join(row2))

if __name__ == "__main__":
    main()
