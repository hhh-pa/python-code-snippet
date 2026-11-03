import sys

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def graham_scan(pts):
    pts = sorted(list(set(pts)))
    if len(pts) <= 2:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    lower.pop()
    upper.pop()
    return lower + upper

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    pts = []
    for _ in range(n):
        pts.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    hull = graham_scan(pts)
    if hull:
        min_idx = 0
        for i in range(1, len(hull)):
            if hull[i] < hull[min_idx]:
                min_idx = i
        hull = hull[min_idx:] + hull[:min_idx]

    out = [str(len(hull))]
    for p in hull:
        out.append(f"{p[0]} {p[1]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
