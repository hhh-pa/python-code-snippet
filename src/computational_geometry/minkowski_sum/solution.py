import sys

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    A = []
    for _ in range(n):
        A.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    m = int(tokens[idx])
    idx += 1
    B = []
    for _ in range(m):
        B.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    pts = set()
    for a in A:
        for b in B:
            pts.add((a[0] + b[0], a[1] + b[1]))

    sorted_pts = sorted(pts)

    lo = []
    for q in sorted_pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)

    hi = []
    for q in reversed(sorted_pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)

    lo.pop()
    hi.pop()
    hull = lo + hi

    out = [str(len(hull))]
    for p in hull:
        out.append(f"{p[0]} {p[1]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
