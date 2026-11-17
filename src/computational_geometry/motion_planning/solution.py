"""motion_planning: Berg 13.2 trapezoidal road map for rectangles + BFS.

Free space = box interior minus closed obstacle rectangles. Faces are
grid cells merged across open boundaries; vertical extensions from
obstacle corners become roadmap nodes linked to adjacent face
centers. Queries locate start/goal faces and run BFS on the roadmap.
All coordinates are doubled so centers and midpoints stay integral.
"""

import collections
import sys


def _compress(box, rects):
    bx0, by0, bx1, by1 = box
    xs = sorted({bx0, bx1} | {x for r in rects for x in (r[0], r[2])})
    ys = sorted({by0, by1} | {y for r in rects for y in (r[1], r[3])})
    return xs, ys


def _blocked_grid(xs, ys, rects):
    nx, ny = len(xs) - 1, len(ys) - 1
    blocked = [[False] * ny for _ in range(nx)]
    for i in range(nx):
        for j in range(ny):
            blocked[i][j] = any(
                rx0 <= xs[i] and xs[i + 1] <= rx1 and ry0 <= ys[j] and ys[j + 1] <= ry1
                for rx0, ry0, rx1, ry1 in rects
            )
    return blocked


def _cast_rays(box, rects):
    bx0, by0, bx1, by1 = box
    rays = []
    for rx0, ry0, rx1, ry1 in rects:
        for ex in (rx0, rx1):
            if bx0 < ex < bx1:
                _cast_edge(rects, by0, by1, ex, ry0, ry1, rays)
    return rays


def _cast_edge(rects, by0, by1, ex, ry0, ry1, rays):
    spanning = [y for r in rects for y in (r[1], r[3]) if r[0] < ex < r[2]]
    hits = [y for y in [*spanning, by1] if y > ry1]
    if hits:
        rays.append((ex, ry1, min(hits)))
    hits = [y for y in [*spanning, by0] if y < ry0]
    if hits:
        rays.append((ex, max(hits), ry0))


def _vsealed(xs, ys, rects, rays, k, j):
    x = xs[k]
    edge = any(
        (rx0 == x or rx1 == x) and ry0 <= ys[j] and ys[j + 1] <= ry1
        for rx0, ry0, rx1, ry1 in rects
    )
    ray = any(ex == x and lo <= ys[j] and ys[j + 1] <= hi for ex, lo, hi in rays)
    return edge or ray


def _hsealed(xs, ys, rects, i, k):
    y = ys[k]
    return any(
        (ry0 == y or ry1 == y) and rx0 <= xs[i] and xs[i + 1] <= rx1
        for rx0, ry0, rx1, ry1 in rects
    )


def _neighbors_open(xs, ys, rects, rays, a, b, nx, ny):
    cands = [
        (a - 1, b, a > 0 and not _vsealed(xs, ys, rects, rays, a, b)),
        (a + 1, b, a + 1 < nx and not _vsealed(xs, ys, rects, rays, a + 1, b)),
        (a, b - 1, b > 0 and not _hsealed(xs, ys, rects, a, b)),
        (a, b + 1, b + 1 < ny and not _hsealed(xs, ys, rects, a, b + 1)),
    ]
    return [(na, nb) for na, nb, ok in cands if ok]


def _flood(xs, ys, rects, rays, blocked, face, ident, i, j, nx, ny):
    dq = collections.deque([(i, j)])
    face[i][j] = ident
    while dq:
        a, b = dq.popleft()
        for na, nb in _neighbors_open(xs, ys, rects, rays, a, b, nx, ny):
            if not blocked[na][nb] and face[na][nb] < 0:
                face[na][nb] = ident
                dq.append((na, nb))


def _paint_faces(xs, ys, rects, rays, blocked):
    nx, ny = len(xs) - 1, len(ys) - 1
    face = [[-1] * ny for _ in range(nx)]
    nfaces = 0
    for i in range(nx):
        for j in range(ny):
            if not blocked[i][j] and face[i][j] < 0:
                _flood(xs, ys, rects, rays, blocked, face, nfaces, i, j, nx, ny)
                nfaces += 1
    return face, nfaces


def _face_centers(xs, ys, face, nfaces):
    nx, ny = len(xs) - 1, len(ys) - 1
    boxes = [[nx, -1, ny, -1] for _ in range(nfaces)]
    for i in range(nx):
        for j in range(ny):
            f = face[i][j]
            if f >= 0:
                b = boxes[f]
                b[0] = min(b[0], i)
                b[1] = max(b[1], i)
                b[2] = min(b[2], j)
                b[3] = max(b[3], j)
    return [(xs[b[0]] + xs[b[1] + 1], ys[b[2]] + ys[b[3] + 1]) for b in boxes]


def _link_ray(xs, ys, face, ny, adj, nfaces, e, ray):
    ex, lo, hi = ray
    k = xs.index(ex)
    sides = set()
    for j in range(ny):
        if lo <= ys[j] and ys[j + 1] <= hi:
            for f in (face[k - 1][j], face[k][j]):
                if f >= 0:
                    sides.add(f)
    node = nfaces + e
    for f in sides:
        adj[f].append(node)
        adj[node].append(f)


def _roadmap(xs, ys, face, rays, nfaces):
    ny = len(ys) - 1
    coords = _face_centers(xs, ys, face, nfaces)
    coords += [(2 * ex, lo + hi) for ex, lo, hi in rays]
    adj = [[] for _ in range(nfaces + len(rays))]
    for e, ray in enumerate(rays):
        _link_ray(xs, ys, face, ny, adj, nfaces, e, ray)
    for lst in adj:
        lst.sort(key=lambda v: coords[v])
    return coords, adj


def _locate(xs, ys, face, sx, sy):
    for i in range(len(xs) - 1):
        if not (xs[i] <= sx <= xs[i + 1]):
            continue
        for j in range(len(ys) - 1):
            if ys[j] <= sy <= ys[j + 1] and face[i][j] >= 0:
                return face[i][j]
    return -1


def _valid(box, rects, px, py):
    bx0, by0, bx1, by1 = box
    if not (bx0 < px < bx1 and by0 < py < by1):
        return False
    return not any(
        rx0 <= px <= rx1 and ry0 <= py <= ry1 for rx0, ry0, rx1, ry1 in rects
    )


def _on_ray(rays, px, py):
    return any(ex == px and lo < py < hi for ex, lo, hi in rays)


def _bfs(adj, fs, fg):
    prev = {fs: -1}
    dq = collections.deque([fs])
    while dq and fg not in prev:
        v = dq.popleft()
        for w in adj[v]:
            if w not in prev:
                prev[w] = v
                dq.append(w)
    if fg not in prev:
        return None
    path = [fg]
    while path[-1] != fs:
        path.append(prev[path[-1]])
    return path


def _answer(box, rects, xs, ys, face, coords, adj, rays, sx, sy, gx, gy):
    if not _valid(box, rects, sx, sy) or not _valid(box, rects, gx, gy):
        return ["FORBIDDEN"]
    if _on_ray(rays, sx, sy) or _on_ray(rays, gx, gy):
        return ["FORBIDDEN"]
    fs = _locate(xs, ys, face, sx, sy)
    fg = _locate(xs, ys, face, gx, gy)
    if fs < 0 or fg < 0:
        return ["FORBIDDEN"]
    if fs == fg:
        pts = [(2 * sx, 2 * sy), (2 * gx, 2 * gy)]
    else:
        path = _bfs(adj, fs, fg)
        if path is None:
            return ["NO PATH"]
        mid = [coords[v] for v in reversed(path)]
        pts = [(2 * sx, 2 * sy), *mid, (2 * gx, 2 * gy)]
    return [str(len(pts))] + [f"{x} {y}" for x, y in pts]


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    box = tuple(data[0:4])
    m = data[4]
    rects = [tuple(data[5 + 4 * i : 9 + 4 * i]) for i in range(m)]
    pos = 5 + 4 * m
    q = data[pos] if pos < len(data) else 0
    queries = [tuple(data[pos + 1 + 4 * i : pos + 5 + 4 * i]) for i in range(q)]
    xs, ys = _compress(box, rects)
    blocked = _blocked_grid(xs, ys, rects)
    rays = _cast_rays(box, rects)
    face, nfaces = _paint_faces(xs, ys, rects, rays, blocked)
    coords, adj = _roadmap(xs, ys, face, rays, nfaces)
    out = []
    for sx, sy, gx, gy in queries:
        out.extend(_answer(box, rects, xs, ys, face, coords, adj, rays, sx, sy, gx, gy))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
