import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        adj[u].append((v, w))

    INF = 4 * 10**18
    dist = [INF] * n
    dist[s] = 0

    inq = [False] * n
    cnt = [0] * n
    par = [-1] * n

    q = deque([s])
    inq[s] = True

    def cyc(v):
        x = v
        for _ in range(n + 1):
            x = par[x]
            if x == -1:
                return False
            if x == v:
                return True
        return True

    while q:
        u = q.popleft()
        inq[u] = False
        d_u = dist[u]
        for v, w in adj[u]:
            if d_u + w < dist[v]:
                dist[v] = d_u + w
                par[v] = u
                if cyc(v):
                    print("NEGATIVE CYCLE")
                    return
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
                    cnt[v] += 1
                    if cnt[v] >= n:
                        print("NEGATIVE CYCLE")
                        return

    out = []
    for i in range(n):
        if dist[i] >= INF // 2:
            out.append("INF")
        else:
            out.append(str(dist[i]))
    print(" ".join(out))

if __name__ == "__main__":
    main()
