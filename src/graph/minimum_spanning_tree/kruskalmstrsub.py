import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    g_nodes = int(next(it))
    g_edges = int(next(it))

    edges = []
    for _ in range(g_edges):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((w, u, v))

    edges.sort()

    parent = list(range(g_nodes + 1))
    size = [1] * (g_nodes + 1)

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        for node in path:
            parent[node] = x
        return x

    def union(x, y):
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return False
        if size[rx] < size[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        size[rx] += size[ry]
        return True

    min_weight = 0
    for w, u, v in edges:
        if union(u, v):
            min_weight += w

    print(min_weight)

if __name__ == "__main__":
    main()
