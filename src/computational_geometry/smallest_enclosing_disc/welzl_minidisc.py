import sys
import math

def dist_sq(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return dx * dx + dy * dy

def in_disc(d, p):
    return dist_sq(d[0], d[1], float(p[0]), float(p[1])) <= d[2] + 1e-9

def disc_from_2(a, b):
    cx = 0.5 * (a[0] + b[0])
    cy = 0.5 * (a[1] + b[1])
    dx = float(b[0] - a[0])
    dy = float(b[1] - a[1])
    return (cx, cy, 0.25 * (dx * dx + dy * dy))

def disc_from_3(a, b, c):
    bx_i = b[0] - a[0]
    by_i = b[1] - a[1]
    cx_i = c[0] - a[0]
    cy_i = c[1] - a[1]
    det = bx_i * cy_i - by_i * cx_i
    if det == 0:
        d1 = disc_from_2(a, b)
        d2 = disc_from_2(a, c)
        d3 = disc_from_2(b, c)
        best = d1
        if d2[2] > best[2]:
            best = d2
        if d3[2] > best[2]:
            best = d3
        return best
    bx = float(bx_i)
    by = float(by_i)
    cx = float(cx_i)
    cy = float(cy_i)
    b2 = bx * bx + by * by
    c2 = cx * cx + cy * cy
    d = 2.0 * float(det)
    ux = (cy * b2 - by * c2) / d
    uy = (bx * c2 - cx * b2) / d
    return (float(a[0]) + ux, float(a[1]) + uy, ux * ux + uy * uy)

def mini_disc_with_2_points(pts, limit, q1, q2):
    d = disc_from_2(q1, q2)
    for k in range(limit):
        if not in_disc(d, pts[k]):
            d = disc_from_3(q1, q2, pts[k])
    return d

def mini_disc_with_point(pts, limit, q):
    d = disc_from_2(pts[0], q)
    for j in range(1, limit):
        if not in_disc(d, pts[j]):
            d = mini_disc_with_2_points(pts, j, pts[j], q)
    return d

def welzl_mini_disc(pts):
    pts = sorted(list(set(pts)))
    if not pts:
        return (0.0, 0.0, 0.0)
    if len(pts) == 1:
        return (float(pts[0][0]), float(pts[0][1]), 0.0)
    d = disc_from_2(pts[0], pts[1])
    for i in range(2, len(pts)):
        if not in_disc(d, pts[i]):
            d = mini_disc_with_point(pts, i, pts[i])
    return d

def llround(val):
    if val >= 0:
        return int(math.floor(val + 0.5))
    else:
        return int(math.ceil(val - 0.5))

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

    ans = welzl_mini_disc(pts)
    cx_out = llround(ans[0] * 1000.0)
    cy_out = llround(ans[1] * 1000.0)
    r2_out = llround(ans[2] * 1000.0)
    sys.stdout.write(f"{cx_out} {cy_out} {r2_out}\n")

if __name__ == "__main__":
    main()
