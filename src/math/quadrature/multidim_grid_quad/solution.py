# Multidimensional grid quadrature (NR 4.8).
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    f3op = toks[0]
    np_ = 10 if f3op == "P3" else (4 if f3op == "E3" else 5)
    p = [float(v) for v in toks[1:1 + np_]]
    pos = 1 + np_
    x1 = float(toks[pos])
    x2 = float(toks[pos + 1])
    pos += 2

    def read_bound(nparams):
        nonlocal pos
        op = toks[pos]
        pos += 1
        if op == "C":
            v = [float(toks[pos])]
            pos += 1
            return op, v
        v = [float(toks[pos + i]) for i in range(nparams)]
        pos += nparams
        return op, v

    y1op, y1p = read_bound(2)
    y2op, y2p = read_bound(2)
    z1op, z1p = read_bound(3)
    z2op, z2p = read_bound(3)

    def f(x, y, z):
        if f3op == "P3":
            return p[0] + p[1] * x + p[2] * y + p[3] * z + p[4] * x * x + p[5] * y * y + \
                p[6] * z * z + p[7] * x * y + p[8] * x * z + p[9] * y * z
        if f3op == "E3":
            return p[0] * math.exp(p[1] * x + p[2] * y + p[3] * z)
        return p[0] * math.sin(p[1] * x + p[2] * y + p[3] * z + p[4])

    def ylo(x):
        return y1p[0] if y1op == "C" else y1p[0] * x + y1p[1]

    def yhi(x):
        return y2p[0] if y2op == "C" else y2p[0] * x + y2p[1]

    def zlo(x, y):
        return z1p[0] if z1op == "C" else z1p[0] + z1p[1] * x + z1p[2] * y

    def zhi(x, y):
        return z2p[0] if z2op == "C" else z2p[0] + z2p[1] * x + z2p[2] * y

    nq = 10
    eps = 1.0e-14
    gx = [0.0] * nq
    gw = [0.0] * nq
    m = (nq + 1) // 2
    for i in range(m):
        z = math.cos(3.141592654 * (i + 0.75) / (nq + 0.5))
        pp = 0.0
        while True:
            p1 = 1.0
            p2 = 0.0
            for j in range(nq):
                p3 = p2
                p2 = p1
                p1 = ((2.0 * j + 1.0) * z * p2 - j * p3) / (j + 1)
            pp = nq * (z * p1 - p2) / (z * z - 1.0)
            z1 = z
            z = z1 - p1 / pp
            if abs(z - z1) <= eps:
                break
        gx[i] = -z
        gx[nq - 1 - i] = z
        gw[i] = 2.0 / ((1.0 - z * z) * pp * pp)
        gw[nq - 1 - i] = gw[i]
    ans = 0.0
    for i in range(nq):
        x = 0.5 * (x1 + x2) + 0.5 * (x2 - x1) * gx[i]
        yl = ylo(x)
        yh = yhi(x)
        for j in range(nq):
            y = 0.5 * (yl + yh) + 0.5 * (yh - yl) * gx[j]
            zl = zlo(x, y)
            zh = zhi(x, y)
            inner = 0.0
            for k in range(nq):
                z = 0.5 * (zl + zh) + 0.5 * (zh - zl) * gx[k]
                inner += gw[k] * f(x, y, z)
            ans += gw[i] * gw[j] * 0.125 * (x2 - x1) * (yh - yl) * (zh - zl) * inner
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
