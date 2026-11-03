import sys

INF = 4000000000000000000

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

    src = int(next(it))
    dist = [INF] * n
    dist[src] = 0

    rounds = 0
    for _ in range(n - 1):
        rounds += 1
        ch = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                ch = True
        if not ch:
            break

    neg = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            neg = True
            break

    if neg:
        print("NEGATIVE CYCLE")
        print(f"MESSAGES: {m * n}")
        return

    out = []
    for i in range(n):
        if dist[i] == INF:
            out.append(f"{i} INF")
        else:
            out.append(f"{i} {dist[i]}")
    out.append(f"MESSAGES: {m * rounds}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
