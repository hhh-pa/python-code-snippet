import sys

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, i):
        path = []
        while self.parent[i] != i:
            path.append(i)
            i = self.parent[i]
        for node in path:
            self.parent[node] = i
        return i

    def unite(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False
        if self.rank[root_i] < self.rank[root_j]:
            root_i, root_j = root_j, root_i
        self.parent[root_j] = root_i
        if self.rank[root_i] == self.rank[root_j]:
            self.rank[root_i] += 1
        self.components -= 1
        return True

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    dsu = DSU(n)
    mst_weight = 0
    edges_added = 0

    while dsu.components > 1:
        cheapest = [-1] * n

        for idx, (u, v, w) in enumerate(edges):
            root_u = dsu.find(u)
            root_v = dsu.find(v)
            if root_u == root_v:
                continue

            if cheapest[root_u] == -1 or w < edges[cheapest[root_u]][2]:
                cheapest[root_u] = idx
            if cheapest[root_v] == -1 or w < edges[cheapest[root_v]][2]:
                cheapest[root_v] = idx

        progress = False
        for i in range(n):
            edge_idx = cheapest[i]
            if edge_idx != -1:
                u, v, w = edges[edge_idx]
                if dsu.unite(u, v):
                    mst_weight += w
                    edges_added += 1
                    progress = True

        if not progress:
            break

    if edges_added == n - 1:
        print(mst_weight)
    else:
        print("DISCONNECTED")

if __name__ == "__main__":
    main()
