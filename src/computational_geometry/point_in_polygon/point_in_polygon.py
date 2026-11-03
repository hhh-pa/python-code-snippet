import sys

def cross(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])

def on_segment(a, b, p):
    if cross(a, b, p) != 0:
        return False
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

def classify_point(poly, p):
    winding = 0
    n = len(poly)
    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        if on_segment(a, b, p):
            return "BOUNDARY"
        if a[1] <= p[1]:
            if b[1] > p[1] and cross(a, b, p) > 0:
                winding += 1
        else:
            if b[1] <= p[1] and cross(a, b, p) < 0:
                winding -= 1
    return "INSIDE" if winding != 0 else "OUTSIDE"

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    q = int(tokens[1])
    if n < 3:
        return
    idx = 2
    poly = []
    for _ in range(n):
        poly.append((int(tokens[idx]), int(tokens[idx + 1])))
        idx += 2

    out = []
    for _ in range(q):
        pt = (int(tokens[idx]), int(tokens[idx + 1]))
        idx += 2
        out.append(classify_point(poly, pt))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
