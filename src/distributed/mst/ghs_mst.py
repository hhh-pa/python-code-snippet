import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    parent = list(range(n))

    def find_root(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def unite(a, b):
        ra = find_root(a)
        rb = find_root(b)
        if ra == rb:
            return False
        parent[rb] = ra
        return True

    edge_indices = list(range(m))
    edge_indices.sort(key=lambda i: edges[i][2])

    total_weight = 0
    edges_count = 0
    mst_edges = []

    for idx in edge_indices:
        u, v, w = edges[idx]
        if unite(u, v):
            total_weight += w
            edges_count += 1
            mst_edges.append((min(u, v), max(u, v)))

    mst_edges.sort()

    out = [
        f"GHS MST Weight: {total_weight}",
        f"Edges: {edges_count}",
    ]
    for u, v in mst_edges:
        out.append(f"{u} {v}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
