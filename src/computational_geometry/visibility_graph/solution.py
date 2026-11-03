import sys
import math

def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def proper_cross(a, b, c, d):
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    return (((o1 > 0) != (o2 > 0)) and o1 != 0 and o2 != 0 and
            ((o3 > 0) != (o4 > 0)) and o3 != 0 and o4 != 0)

def on_open(p, a, b):
    if orient(a, b, p) != 0:
        return False
    return (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1]) < 0

def on_closed2(px, py, a, b):
    ax = 2 * a[0]
    ay = 2 * a[1]
    bx = 2 * b[0]
    by = 2 * b[1]
    if (bx - ax) * (py - ay) - (by - ay) * (px - ax) != 0:
        return False
    return (min(ax, bx) <= px <= max(ax, bx) and
            min(ay, by) <= py <= max(ay, by))

def pip_strict(X, Y, P):
    m = len(P)
    for i in range(m):
        if on_closed2(X, Y, P[i], P[(i + 1) % m]):
            return False
    inside = False
    for i in range(m):
        cx = 2 * P[i][0]
        cy = 2 * P[i][1]
        dx = 2 * P[(i + 1) % m][0]
        dy = 2 * P[(i + 1) % m][1]
        if (cy > Y) != (dy > Y):
            if dy > cy:
                cond = X * (dy - cy) < cx * (dy - cy) + (dx - cx) * (Y - cy)
            else:
                cond = X * (dy - cy) > cx * (dy - cy) + (dx - cx) * (Y - cy)
            if cond:
                inside = not inside
    return inside

def visible(a, b, obs):
    for P in obs:
        m = len(P)
        for i in range(m):
            if proper_cross(a, b, P[i], P[(i + 1) % m]):
                return False
        for v in P:
            if on_open(v, a, b):
                if pip_strict(a[0] + v[0], a[1] + v[1], P):
                    return False
                if pip_strict(v[0] + b[0], v[1] + b[1], P):
                    return False
    return True

def ew(a, b):
    dx = float(a[0] - b[0])
    dy = float(a[1] - b[1])
    return math.hypot(dx, dy)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    obs = []
    for _ in range(n):
        k = int(tokens[idx])
        idx += 1
        poly = []
        for _ in range(k):
            poly.append((int(tokens[idx]), int(tokens[idx + 1])))
            idx += 2
        obs.append(poly)

    s = (int(tokens[idx]), int(tokens[idx + 1]))
    t = (int(tokens[idx + 2]), int(tokens[idx + 3]))
    idx += 4

    pts = [s, t]
    for P in obs:
        for v in P:
            pts.append(v)

    V = len(pts)
    E = []
    W = [[-1.0] * V for _ in range(V)]
    for i in range(V):
        for j in range(i + 1, V):
            if visible(pts[i], pts[j], obs):
                E.append((i, j))
                d = ew(pts[i], pts[j])
                W[i][j] = d
                W[j][i] = d

    out = [str(len(E))]
    for e in E:
        out.append(f"{e[0]} {e[1]}")

    INF = float('inf')
    dist = [INF] * V
    prev = [-1] * V
    used = [False] * V
    dist[0] = 0.0

    for _ in range(V):
        u = -1
        for i in range(V):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == INF:
            break
        used[u] = True
        if u == 1:
            break
        for v in range(V):
            if W[u][v] < 0 or used[v]:
                continue
            nd = dist[u] + W[u][v]
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u

    if dist[1] == INF:
        out.extend(["0", "", "-1"])
        sys.stdout.write("\n".join(out) + "\n")
        return

    path = []
    curr = 1
    while curr != -1:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    out.append(str(len(path)))
    out.append(" ".join(str(v) for v in path))
    out.append(f"{dist[1]:.6f}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
