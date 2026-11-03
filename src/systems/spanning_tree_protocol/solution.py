import sys

INFLL = 4000000000000000000

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        B = int(next(it))
        E = int(next(it))
    except StopIteration:
        return

    links = []
    adj = [[] for _ in range(B)]
    for _ in range(E):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        links.append((u, v, c))
        adj[u].append((v, c))
        adj[v].append((u, c))

    root = 0
    dist = [INFLL] * B
    done = [False] * B
    dist[root] = 0

    for _ in range(B):
        u = -1
        for i in range(B):
            if not done[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == INFLL:
            break
        done[u] = True
        for v, c in adj[u]:
            if dist[u] + c < dist[v]:
                dist[v] = dist[u] + c

    out = [str(root)]
    for b in range(B):
        if b == root:
            out.append("-1")
        elif dist[b] == INFLL:
            out.append("-2")
        else:
            best = -1
            for nb, c in adj[b]:
                if dist[nb] + c == dist[b] and (best == -1 or nb < best):
                    best = nb
            out.append(str(best))

    for u, v, c in links:
        if dist[u] < dist[v]:
            d = u
        elif dist[v] < dist[u]:
            d = v
        else:
            d = min(u, v)
        out.append(str(d))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
