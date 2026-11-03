import sys
from collections import deque

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def inside(p, a, b, c):
    c1 = cross(a, b, p)
    c2 = cross(b, c, p)
    c3 = cross(c, a, p)
    return c1 > 0 and c2 > 0 and c3 > 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pin = []
    for _ in range(n):
        pin.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    area2 = 0
    for i in range(n):
        a = pin[i]
        b = pin[(i + 1) % n]
        area2 += a[0] * b[1] - a[1] * b[0]

    pts = list(pin)
    w2o = list(range(n))
    if area2 < 0:
        pts.reverse()
        for i in range(n):
            w2o[i] = n - 1 - i

    poly = list(range(n))
    tris = []

    def convex(a, b, c):
        return cross(pts[a], pts[b], pts[c]) > 0

    while len(poly) > 3:
        m = len(poly)
        found = -1
        for k in range(m):
            a = poly[(k - 1 + m) % m]
            b = poly[k]
            c = poly[(k + 1) % m]
            if not convex(a, b, c):
                continue
            ok = True
            for v in poly:
                if v == a or v == b or v == c:
                    continue
                if inside(pts[v], pts[a], pts[b], pts[c]):
                    ok = False
                    break
            if ok:
                found = k
                break
        m2 = len(poly)
        a = poly[(found - 1 + m2) % m2]
        b = poly[found]
        c = poly[(found + 1) % m2]
        tris.append([a, b, c])
        poly.pop(found)

    tris.append([poly[0], poly[1], poly[2]])

    emap = {}
    for t in range(len(tris)):
        for e in range(3):
            u = tris[t][e]
            v = tris[t][(e + 1) % 3]
            if u > v:
                u, v = v, u
            emap.setdefault((u, v), []).append(t)

    color = [-1] * n
    color[tris[0][0]] = 0
    color[tris[0][1]] = 1
    color[tris[0][2]] = 2

    vis = [False] * len(tris)
    vis[0] = True
    q = deque([0])

    while q:
        t = q.popleft()
        for e in range(3):
            u = tris[t][e]
            v = tris[t][(e + 1) % 3]
            a, b = (v, u) if u > v else (u, v)
            for s in emap.get((a, b), []):
                if not vis[s]:
                    vis[s] = True
                    w = -1
                    for x in tris[s]:
                        if x != u and x != v:
                            w = x
                    color[w] = 3 - color[u] - color[v]
                    q.append(s)

    cls = [[], [], []]
    for i in range(n):
        cls[color[i]].append(i)
    for c in range(3):
        cls[c].sort()

    best = 0
    for c in range(1, 3):
        if len(cls[c]) < len(cls[best]) or (len(cls[c]) == len(cls[best]) and cls[c] < cls[best]):
            best = c

    guards = [w2o[w] for w in cls[best]]
    guards.sort()

    out = [str(len(guards)), " ".join(str(g) for g in guards)]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
