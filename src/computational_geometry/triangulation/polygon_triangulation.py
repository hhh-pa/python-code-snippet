import sys

EPS = 1e-9

def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def point_in_triangle(p, a, b, c):
    cp1 = cross(a, b, p)
    cp2 = cross(b, c, p)
    cp3 = cross(c, a, p)
    has_neg = (cp1 < -EPS) or (cp2 < -EPS) or (cp3 < -EPS)
    has_pos = (cp1 > EPS) or (cp2 > EPS) or (cp3 > EPS)
    return not (has_neg and has_pos)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    poly = []
    for i in range(n):
        x = float(tokens[idx])
        y = float(tokens[idx + 1])
        idx += 2
        poly.append((x, y, i))

    signed_area = 0.0
    for i in range(len(poly)):
        next_i = (i + 1) % len(poly)
        signed_area += poly[i][0] * poly[next_i][1] - poly[next_i][0] * poly[i][1]
    if signed_area < 0:
        poly.reverse()

    triangles = []
    while len(poly) > 3:
        ear_found = False
        sz = len(poly)
        for i in range(sz):
            prev_i = (i + sz - 1) % sz
            next_i = (i + 1) % sz

            a = poly[prev_i]
            b = poly[i]
            c = poly[next_i]

            if cross(a, b, c) <= EPS:
                continue

            is_ear = True
            for j in range(sz):
                if j == prev_i or j == i or j == next_i:
                    continue
                if point_in_triangle(poly[j], a, b, c):
                    is_ear = False
                    break

            if is_ear:
                tri = sorted([a[2], b[2], c[2]])
                triangles.append(tuple(tri))
                poly.pop(i)
                ear_found = True
                break

        if not ear_found:
            break

    if len(poly) == 3:
        tri = sorted([poly[0][2], poly[1][2], poly[2][2]])
        triangles.append(tuple(tri))

    triangles.sort()
    out = [str(len(triangles))]
    for tri in triangles:
        out.append(f"{tri[0]} {tri[1]} {tri[2]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
