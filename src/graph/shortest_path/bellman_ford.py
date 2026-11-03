import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    v_count = int(next(it))
    e_count = int(next(it))
    start_node = int(next(it))

    edges = []
    for _ in range(e_count):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    INF = 10**18
    dist = [INF] * v_count
    parent = [-1] * v_count
    dist[start_node] = 0

    last_relaxed = -1
    for _ in range(v_count):
        last_relaxed = -1
        for u, v, w in edges:
            if dist[u] < INF:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    last_relaxed = v
        if last_relaxed == -1:
            break

    if last_relaxed != -1:
        cycle_node = last_relaxed
        for _ in range(v_count):
            cycle_node = parent[cycle_node]

        cycle = []
        cur = cycle_node
        while True:
            cycle.append(cur)
            if cur == cycle_node and len(cycle) > 1:
                break
            cur = parent[cur]
        cycle.reverse()

        print("NEGATIVE CYCLE")
        print(" ".join(str(x) for x in cycle))
    else:
        out = []
        for i in range(v_count):
            if dist[i] >= INF // 2:
                out.append("INF")
            else:
                out.append(str(dist[i]))
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
