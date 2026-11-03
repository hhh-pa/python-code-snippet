import sys
import math

sys.setrecursionlimit(200000)

def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)

def closest_pair_rec(pts_x, l, r):
    if r - l <= 3:
        min_d = 1e18
        for i in range(l, r):
            for j in range(i + 1, r):
                d = dist(pts_x[i], pts_x[j])
                if d < min_d:
                    min_d = d
        return min_d

    mid = l + (r - l) // 2
    mid_x = pts_x[mid][0]

    d1 = closest_pair_rec(pts_x, l, mid)
    d2 = closest_pair_rec(pts_x, mid, r)
    d = min(d1, d2)

    strip = [pts_x[i] for i in range(l, r) if abs(pts_x[i][0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])

    m = len(strip)
    for i in range(m):
        for j in range(i + 1, m):
            if strip[j][1] - strip[i][1] >= d:
                break
            cur_d = dist(strip[i], strip[j])
            if cur_d < d:
                d = cur_d

    return d

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((float(tokens[idx]), float(tokens[idx + 1])))
        idx += 2

    pts.sort(key=lambda p: (p[0], p[1]))

    ans = closest_pair_rec(pts, 0, len(pts))
    sys.stdout.write(f"{ans:.6f}\n")

if __name__ == "__main__":
    main()
