import sys

EPS = 1e-9

def circumcircle(a, b, c):
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < EPS:
        return None, 0.0

    a2 = a[0] * a[0] + a[1] * a[1]
    b2 = b[0] * b[0] + b[1] * b[1]
    c2 = c[0] * c[0] + c[1] * c[1]

    ux = (a2 * (b[1] - c[1]) + b2 * (c[1] - a[1]) + c2 * (a[1] - b[1])) / d
    uy = (a2 * (c[0] - b[0]) + b2 * (a[0] - c[0]) + c2 * (b[0] - a[0])) / d

    r_sq = (a[0] - ux) * (a[0] - ux) + (a[1] - uy) * (a[1] - uy)
    return (ux, uy), r_sq

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

    centers = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                center, r_sq = circumcircle(pts[i], pts[j], pts[k])
                if center is None:
                    continue

                valid = True
                for m in range(n):
                    if m == i or m == j or m == k:
                        continue
                    dx = pts[m][0] - center[0]
                    dy = pts[m][1] - center[1]
                    dist_sq = dx * dx + dy * dy
                    if dist_sq < r_sq - EPS:
                        valid = False
                        break

                if valid:
                    centers.append(center)

    centers.sort()
    unique_centers = []
    for c in centers:
        if not unique_centers:
            unique_centers.append(c)
        else:
            prev = unique_centers[-1]
            if abs(c[0] - prev[0]) > EPS or abs(c[1] - prev[1]) > EPS:
                unique_centers.append(c)

    out = [str(len(unique_centers))]
    for v in unique_centers:
        out.append(f"{v[0]:.2f} {v[1]:.2f}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
