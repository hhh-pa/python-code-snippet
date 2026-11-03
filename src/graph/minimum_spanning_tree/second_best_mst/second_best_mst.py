import sys
from collections import deque

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        path = []
        while self.p[x] != x:
            path.append(x)
            x = self.p[x]
        for node in path:
            self.p[node] = x
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
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

    o = list(range(m))
    o.sort(key=lambda i: (edges[i][2], edges[i][0], edges[i][1]))

    d = DSU(n)
    used = [False] * m
    mw = 0
    cnt = 0

    for i in o:
        u, v, w = edges[i]
        if d.union(u, v):
            used[i] = True
            mw += w
            cnt += 1

    if cnt != n - 1:
        print("DISCONNECTED")
        return

    ta = [[] for _ in range(n)]
    for i in range(m):
        if used[i]:
            u, v, w = edges[i]
            ta[u].append((v, w))
            ta[v].append((u, w))

    def maxe(s, t):
        if s == t:
            return 0
        par = [-1] * n
        pw = [0] * n
        q = deque([s])
        par[s] = s
        while q:
            u = q.popleft()
            if u == t:
                break
            for w_node, c in ta[u]:
                if par[w_node] == -1:
                    par[w_node] = u
                    pw[w_node] = c
                    q.append(w_node)
        mx = 0
        x = t
        while x != s:
            if pw[x] > mx:
                mx = pw[x]
            x = par[x]
        return mx

    best = float('inf')
    any_found = False

    for i in range(m):
        if not used[i]:
            u, v, w = edges[i]
            c = mw + w - maxe(u, v)
            if not any_found or c < best:
                best = c
                any_found = True

    print(mw)
    if any_found:
        print(best)
    else:
        print("NO SECOND")

if __name__ == "__main__":
    main()
