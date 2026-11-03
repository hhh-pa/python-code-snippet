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
    t = int(next(it))

    res = [[0] * n for _ in range(n)]
    cost = [[0] * n for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        w = int(next(it))
        res[u][v] += c
        cost[u][v] = w
        cost[v][u] = -w

    INF = 4 * 10**18
    pi = [0] * n
    for _ in range(n):
        for u in range(n):
            for v in range(n):
                if res[u][v] > 0 and pi[u] + cost[u][v] < pi[v]:
                    pi[v] = pi[u] + cost[u][v]

    flow = 0
    tot = 0

    while True:
        dist = [INF] * n
        par = [-1] * n
        dist[s] = 0
        h = [(0, s)]
        while h:
            du, u = heapq.heappop(h)
            if du != dist[u]:
                continue
            for v in range(n):
                if res[u][v] > 0:
                    rc = cost[u][v] + pi[u] - pi[v]
                    if dist[u] + rc < dist[v]:
                        dist[v] = dist[u] + rc
                        par[v] = u
                        heapq.heappush(h, (dist[v], v))

        if par[t] == -1:
            break

        for v in range(n):
            if dist[v] < INF:
                pi[v] += dist[v]

        b = INF
        v = t
        while v != s:
            p = par[v]
            if res[p][v] < b:
                b = res[p][v]
            v = p

        v = t
        while v != s:
            p = par[v]
            res[p][v] -= b
            res[v][p] += b
            tot += b * cost[p][v]
            v = p

        flow += b

    print(f"{flow} {tot}")

if __name__ == "__main__":
    main()
