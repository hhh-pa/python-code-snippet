import sys
import math

def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def perimeter(p):
    if not p:
        return 0.0
    ans = 0.0
    for i in range(len(p) - 1):
        ans += dist(p[i], p[i + 1])
    ans += dist(p[0], p[-1])
    return ans

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def hull(points):
    ans = []
    for p in points:
        while len(ans) >= 2 and cross(ans[-2], ans[-1], p) <= 0:
            ans.pop()
        ans.append(p)
    if ans:
        ans.pop()
    return ans

def convex_hull(points):
    distinct_points = sorted(list(set(points)))
    if len(distinct_points) > 2:
        lower = hull(distinct_points)
        upper = hull(list(reversed(distinct_points)))
        return lower + upper
    return distinct_points

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    points = []
    for _ in range(n):
        points.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    ans = perimeter(convex_hull(points))
    sys.stdout.write(f"{ans:.1f}\n")

if __name__ == "__main__":
    main()
