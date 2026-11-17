# https://leetcode.com/problems/is-graph-bipartite/
import sys


def is_bipartite(adj):
    color = [-1] * len(adj)
    for s in range(len(adj)):
        if color[s] != -1:
            continue
        color[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if color[w] == -1:
                    color[w] = 1 - color[u]
                    stack.append(w)
                elif color[w] == color[u]:
                    return False
    return True


def main():
    data = list(map(int, sys.stdin.read().split()))
    if len(data) < 2 or data[0] < 0 or data[1] < 0:
        return
    n, m = data[0], data[1]
    vals = data[2:]
    edges = [(vals[2 * i], vals[2 * i + 1]) for i in range(min(m, len(vals) // 2))]
    if any(u == v for u, v in edges):
        print(0)
        return
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            adj[v].append(u)
    print(1 if is_bipartite(adj) else 0)


if __name__ == "__main__":
    main()
