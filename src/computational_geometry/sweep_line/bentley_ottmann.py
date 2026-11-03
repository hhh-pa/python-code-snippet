import sys

EPS = 1e-9

def intersect(s1, s2):
    x1, y1 = s1[0]
    x2, y2 = s1[1]
    x3, y3 = s2[0]
    x4, y4 = s2[1]

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < EPS:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    if -EPS <= t <= 1.0 + EPS and -EPS <= u <= 1.0 + EPS:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    segs = []
    for _ in range(n):
        x1 = float(tokens[idx])
        y1 = float(tokens[idx + 1])
        x2 = float(tokens[idx + 2])
        y2 = float(tokens[idx + 3])
        idx += 4
        p1 = (x1, y1)
        p2 = (x2, y2)
        if (p2[0] < p1[0] - EPS) or (abs(p2[0] - p1[0]) <= EPS and p2[1] < p1[1] - EPS):
            p1, p2 = p2, p1
        segs.append((p1, p2))

    pts = []
    for i in range(n):
        for j in range(i + 1, n):
            pt = intersect(segs[i], segs[j])
            if pt is not None:
                pts.append(pt)

    pts.sort()
    unique_pts = []
    for pt in pts:
        if not unique_pts:
            unique_pts.append(pt)
        else:
            prev = unique_pts[-1]
            if abs(pt[0] - prev[0]) > EPS or abs(pt[1] - prev[1]) > EPS:
                unique_pts.append(pt)

    out = [str(len(unique_pts))]
    for pt in unique_pts:
        out.append(f"{pt[0]:.2f} {pt[1]:.2f}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
