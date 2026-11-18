"""Christofides 3/2 TSP: MST + subset-DP matching + Euler + shortcut."""

import math
import sys


def _mst(n, w):
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    edges = sorted([(w[i][j], i, j) for i in range(n) for j in range(i + 1, n)])
    mst = []
    for _, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            mst.append((u, v))
    return mst


def _odd_vertices(n, mst):
    deg = [0] * n
    for u, v in mst:
        deg[u] += 1
        deg[v] += 1
    return [i for i in range(n) if deg[i] % 2]


def _match_dp(odd, w):
    k = len(odd)
    inf = float("inf")
    dp = [inf] * (1 << k)
    choice = [0] * (1 << k)
    dp[0] = 0.0
    for mask in range(1, 1 << k):
        i = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << i)
        best, bj = inf, -1
        for j in range(i + 1, k):
            if rest & (1 << j):
                c = w[odd[i]][odd[j]] + dp[rest ^ (1 << j)]
                if c < best:
                    best, bj = c, j
        dp[mask] = best
        choice[mask] = bj
    return choice


def _euler_tour(n, mst, odd, choice):
    adj = [[] for _ in range(n)]
    enum = [0]

    def add_edge(u, v):
        adj[u].append((v, enum[0]))
        adj[v].append((u, enum[0]))
        enum[0] += 1

    for u, v in mst:
        add_edge(u, v)
    mask = (1 << len(odd)) - 1
    while mask:
        i = (mask & -mask).bit_length() - 1
        j = choice[mask]
        add_edge(odd[i], odd[j])
        mask ^= (1 << i) ^ (1 << j)
    for lst in adj:
        lst.sort(key=lambda e: e[0], reverse=True)
    used = [False] * enum[0]
    stack, tour = [0], []
    while stack:
        v = stack[-1]
        while adj[v] and used[adj[v][-1][1]]:
            adj[v].pop()
        if adj[v]:
            u, e = adj[v].pop()
            used[e] = True
            stack.append(u)
        else:
            tour.append(stack.pop())
    tour.reverse()
    return tour


def _christofides(n, w):
    mst = _mst(n, w)
    odd = _odd_vertices(n, mst)
    choice = _match_dp(odd, w)
    tour = _euler_tour(n, mst, odd, choice)
    seen = set()
    short = []
    for v in tour:
        if v not in seen:
            seen.add(v)
            short.append(v)
    length = sum(w[short[i]][short[(i + 1) % n]] for i in range(n))
    return short, length


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    kind = toks[1]
    vals = list(map(float, toks[2:]))
    if kind == "LINE":
        xs = vals[:n]
        w = [[abs(xs[i] - xs[j]) for j in range(n)] for i in range(n)]
    else:
        pts = [(vals[2 * i], vals[2 * i + 1]) for i in range(n)]
        w = []
        for i in range(n):
            row = []
            for j in range(n):
                dx = pts[i][0] - pts[j][0]
                dy = pts[i][1] - pts[j][1]
                row.append(math.sqrt(dx * dx + dy * dy))
            w.append(row)
    tour, length = _christofides(n, w)
    sys.stdout.write(" ".join(map(str, tour)) + f"\n{length:.6f}")


if __name__ == "__main__":
    main()
