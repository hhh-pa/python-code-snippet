import sys

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def build_hull(p, q, pts, out):
    if not pts:
        return
    best_idx = 0
    best_dist = cross(q, p, pts[0])
    for i in range(1, len(pts)):
        d = cross(q, p, pts[i])
        if d > best_dist or (d == best_dist and pts[i] < pts[best_idx]):
            best_dist = d
            best_idx = i

    c = pts[best_idx]
    left_pc = []
    left_cq = []
    for pt in pts:
        if cross(c, p, pt) > 0:
            left_pc.append(pt)
        elif cross(q, c, pt) > 0:
            left_cq.append(pt)

    build_hull(p, c, left_pc, out)
    out.append(c)
    build_hull(c, q, left_cq, out)

def quickhull(pts):
    pts = sorted(list(set(pts)))
    if len(pts) <= 2:
        return pts

    a = pts[0]
    b = pts[-1]
    lower_pts = []
    upper_pts = []
    for i in range(1, len(pts) - 1):
        cp = cross(a, b, pts[i])
        if cp < 0:
            lower_pts.append(pts[i])
        elif cp > 0:
            upper_pts.append(pts[i])

    if not lower_pts and not upper_pts:
        return [a, b]

    raw = [a]
    build_hull(a, b, lower_pts, raw)
    raw.append(b)
    build_hull(b, a, upper_pts, raw)

    hull = []
    m = len(raw)
    for i in range(m):
        prev = raw[(i + m - 1) % m]
        curr = raw[i]
        nxt = raw[(i + 1) % m]
        if cross(prev, curr, nxt) > 0:
            hull.append(curr)

    if hull:
        min_idx = 0
        for i in range(1, len(hull)):
            if hull[i] < hull[min_idx]:
                min_idx = i
        hull = hull[min_idx:] + hull[:min_idx]
    return hull

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n <= 0:
        return
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    hull = quickhull(pts)
    out = []
    for p in hull:
        out.append(f"{p[0]} {p[1]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
