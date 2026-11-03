import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))

    adj = [[] for _ in range(n)]
    cmax = 0
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        adj[u].append((v, w))
        if w > cmax:
            cmax = w

    INF = 4 * 10**18
    dist = [INF] * n
    dist[s] = 0

    maxd = max(1, (n - 1) * cmax)
    bk = [[] for _ in range(maxd + 1)]
    bk[0].append(s)

    done = [False] * n
    idx = 0
    pending = 1

    while pending > 0:
        while idx <= maxd and not bk[idx]:
            idx += 1
        if idx > maxd:
            break
        u = bk[idx].pop()
        if done[u]:
            continue
        done[u] = True
        d_u = dist[u]
        for v, w in adj[u]:
            if d_u + w < dist[v]:
                dist[v] = d_u + w
                bk[dist[v]].append(v)
                pending += 1
        pending -= 1

    out = []
    for i in range(n):
        if dist[i] >= INF // 2:
            out.append("INF")
        else:
            out.append(str(dist[i]))
    print(" ".join(out))

if __name__ == "__main__":
    main()
