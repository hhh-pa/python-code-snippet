import sys
import math
from collections import deque
from functools import cmp_to_key

class HalfPlane:
    def __init__(self, dx, dy, c):
        self.dx = dx
        self.dy = dy
        self.c = c

    def half(self):
        return 0 if (self.dy > 0 or (self.dy == 0 and self.dx > 0)) else 1

def cmp_hp(h1, h2):
    half1 = h1.half()
    half2 = h2.half()
    if half1 != half2:
        return -1 if half1 < half2 else 1
    cr = h1.dx * h2.dy - h1.dy * h2.dx
    if cr != 0:
        return -1 if cr > 0 else 1
    if h1.c != h2.c:
        return -1 if h1.c > h2.c else 1
    return 0

def is_outside(h, p):
    lhs = -h.dy * p[0] + h.dx * p[1]
    return lhs < h.c - 1e-9

def intersect(h1, h2):
    det = float(h1.dx * h2.dy - h1.dy * h2.dx)
    c1 = float(h1.c)
    c2 = float(h2.c)
    x = (c1 * float(h2.dx) - float(h1.dx) * c2) / det
    y = (c1 * float(h2.dy) - float(h1.dy) * c2) / det
    return (x, y)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n <= 0:
        return
    idx = 1
    raw = []
    for _ in range(n):
        x1 = int(tokens[idx])
        y1 = int(tokens[idx + 1])
        x2 = int(tokens[idx + 2])
        y2 = int(tokens[idx + 3])
        idx += 4
        dx = x2 - x1
        dy = y2 - y1
        g = math.gcd(dx, dy)
        if g == 0:
            continue
        dx //= g
        dy //= g
        c = dx * y1 - dy * x1
        raw.append(HalfPlane(dx, dy, c))

    raw.sort(key=cmp_to_key(cmp_hp))
    hps = []
    for h in raw:
        if not hps or hps[-1].dx != h.dx or hps[-1].dy != h.dy:
            hps.append(h)

    dq = deque()
    for h in hps:
        while len(dq) >= 2 and is_outside(h, intersect(dq[-2], dq[-1])):
            dq.pop()
        while len(dq) >= 2 and is_outside(h, intersect(dq[0], dq[1])):
            dq.popleft()
        if dq and (dq[-1].dx * h.dy - dq[-1].dy * h.dx) == 0:
            sys.stdout.write("0 0\n")
            return
        dq.append(h)

    while len(dq) >= 3 and is_outside(dq[0], intersect(dq[-2], dq[-1])):
        dq.pop()
    while len(dq) >= 3 and is_outside(dq[-1], intersect(dq[0], dq[1])):
        dq.popleft()

    if len(dq) < 3:
        sys.stdout.write("0 0\n")
        return

    m = len(dq)
    verts = []
    for i in range(m):
        h1 = dq[i]
        h2 = dq[(i + 1) % m]
        if (h1.dx * h2.dy - h1.dy * h2.dx) <= 0:
            sys.stdout.write("0 0\n")
            return
        pt = intersect(h1, h2)
        if not verts or math.hypot(pt[0] - verts[-1][0], pt[1] - verts[-1][1]) > 1e-7:
            verts.append(pt)

    if len(verts) >= 2 and math.hypot(verts[0][0] - verts[-1][0], verts[0][1] - verts[-1][1]) <= 1e-7:
        verts.pop()

    if len(verts) < 3:
        sys.stdout.write("0 0\n")
        return

    area2 = 0.0
    v = len(verts)
    for i in range(v):
        a = verts[i]
        b = verts[(i + 1) % v]
        area2 += a[0] * b[1] - a[1] * b[0]

    area = 0.5 * abs(area2)
    if area <= 1e-9:
        sys.stdout.write("0 0\n")
        return

    # In C++: std::llround(area * 1000.0) -> round halfway cases away from zero
    val = area * 1000.0
    if val >= 0:
        area_out = int(math.floor(val + 0.5))
    else:
        area_out = int(math.ceil(val - 0.5))

    sys.stdout.write(f"{v} {area_out}\n")

if __name__ == "__main__":
    main()
