import sys

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

    edges.sort(key=lambda e: (e[2], e[0], e[1]))

    d = DSU(n)
    mw = 0
    bn = 0
    cnt = 0

    for u, v, w in edges:
        if d.union(u, v):
            mw += w
            if w > bn:
                bn = w
            cnt += 1

    if n > 0 and cnt != n - 1:
        print("DISCONNECTED")
        return

    print(bn)
    print(mw)

if __name__ == "__main__":
    main()
