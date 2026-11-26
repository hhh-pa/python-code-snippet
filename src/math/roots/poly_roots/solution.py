# Polynomial roots (NR 9.5).
import math
import sys

MACEPS = 2.220446049250313e-16
FRAC = (0.0, 0.5, 0.25, 0.75, 0.13, 0.38, 0.62, 0.88, 1.0)


def cxadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cxsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cxmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cxdiv(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def cxscale(a, s):
    return (a[0] * s, a[1] * s)


def cxabs(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1])


def cxsqrt(w):
    if w[1] == 0.0:
        if w[0] >= 0.0:
            return (math.sqrt(w[0]), 0.0)
        return (0.0, math.sqrt(-w[0]))
    r = cxabs(w)
    re = math.sqrt((r + w[0]) * 0.5)
    im = math.sqrt((r - w[0]) * 0.5)
    return (re, im if w[1] >= 0.0 else -im)


def cxpolar(r, th):
    return (r * math.cos(th), r * math.sin(th))


def laguer(a, x):
    mr, mt, maxit = 8, 10, 80
    m = len(a) - 1
    its = 0
    for it in range(1, maxit + 1):
        its = it
        b = a[m]
        err = cxabs(b)
        d = (0.0, 0.0)
        f = (0.0, 0.0)
        abx = cxabs(x)
        for j in range(m - 1, -1, -1):
            f = cxadd(cxmul(x, f), d)
            d = cxadd(cxmul(x, d), b)
            b = cxadd(cxmul(x, b), a[j])
            err = cxabs(b) + abx * err
        err *= MACEPS
        if cxabs(b) <= err:
            return x, its, 0
        g = cxdiv(d, b)
        g2 = cxmul(g, g)
        h = cxsub(g2, cxscale(cxdiv(f, b), 2.0))
        sq = cxsqrt(cxscale(cxsub(cxscale(h, float(m)), g2), float(m - 1)))
        gp = cxadd(g, sq)
        gm = cxsub(g, sq)
        abp, abm = cxabs(gp), cxabs(gm)
        if abp < abm:
            gp = gm
        mx = abm if abp < abm else abp
        if mx > 0.0:
            dx = cxdiv((float(m), 0.0), gp)
        else:
            dx = cxpolar(1 + abx, float(it))
        x1 = cxsub(x, dx)
        if x[0] == x1[0] and x[1] == x1[1]:
            return x, its, 0
        if it % mt != 0:
            x = x1
        else:
            x = cxsub(x, cxscale(dx, FRAC[it // mt]))
    return x, its, 1


def poldiv(u, v):
    n = len(u) - 1
    nv = len(v) - 1
    while nv >= 0 and v[nv] == 0.0:
        nv -= 1
    r = list(u)
    q = [0.0] * len(u)
    for k in range(n - nv, -1, -1):
        q[k] = r[nv + k] / v[nv]
        for j in range(nv + k - 1, k - 1, -1):
            r[j] -= q[k] * v[j - k]
    for j in range(nv, n + 1):
        r[j] = 0.0
    return q, r


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    out = []
    if toks[0] == "ZROOTS":
        m = int(toks[1])
        a = [(float(toks[2 + 2 * i]), float(toks[3 + 2 * i])) for i in range(m + 1)]
        polish = int(toks[2 + 2 * (m + 1)])
        eps = 1.0e-14
        ad = list(a)
        roots = [(0.0, 0.0)] * m
        flag = 0
        for j in range(m - 1, -1, -1):
            if flag:
                break
            x, _, flag = laguer(ad[:j + 2], (0.0, 0.0))
            if flag:
                break
            if abs(x[1]) <= 2.0 * eps * abs(x[0]):
                x = (x[0], 0.0)
            roots[j] = x
            b = ad[j + 1]
            for jj in range(j, -1, -1):
                c = ad[jj]
                ad[jj] = b
                b = cxadd(cxmul(x, b), c)
        if not flag and polish:
            for j in range(m):
                if flag:
                    break
                x, _, flag = laguer(a, roots[j])
                roots[j] = x
        if not flag:
            for j in range(1, m):
                x = roots[j]
                i = j - 1
                while i >= 0:
                    if roots[i][0] <= x[0]:
                        break
                    roots[i + 1] = roots[i]
                    i -= 1
                roots[i + 1] = x
        for j in range(m):
            r, s = roots[j] if not flag else (0.0, 0.0)
            out += ["%.6f" % (canon(r) + 0.0), "%.6f" % (canon(s) + 0.0)]
        out.append(str(flag))
    elif toks[0] == "LAGUER":
        m = int(toks[1])
        a = [(float(toks[2 + 2 * i]), float(toks[3 + 2 * i])) for i in range(m + 1)]
        base = 2 + 2 * (m + 1)
        x = (float(toks[base]), float(toks[base + 1]))
        x, its, flag = laguer(a, x)
        if flag:
            out += ["0.000000", "0.000000", "0", "1"]
        else:
            out += ["%.6f" % (canon(x[0]) + 0.0), "%.6f" % (canon(x[1]) + 0.0),
                    str(its), "0"]
    elif toks[0] == "QROOT":
        n = int(toks[1])
        p = [float(w) for w in toks[2:3 + n]]
        b, c, eps = float(toks[3 + n]), float(toks[4 + n]), float(toks[5 + n])
        tiny = 1.0e-14
        d = [0.0, 0.0, 1.0]
        flag = 0
        for it in range(20):
            d[1] = b
            d[0] = c
            q, rem = poldiv(p, d)
            s = rem[0]
            r = rem[1]
            _, rem = poldiv(q, d)
            rc = -rem[1]
            sb = -c * rc
            sc = -rem[0]
            rb = -b * rc + sc
            dv = 1.0 / (sb * rc - sc * rb)
            delb = (r * sc - s * rc) * dv
            delc = (-r * sb + s * rb) * dv
            b += delb
            c += delc
            if (abs(delb) <= eps * abs(b) or abs(b) < tiny) and \
                    (abs(delc) <= eps * abs(c) or abs(c) < tiny):
                break
            if it == 19:
                flag = 1
        if flag:
            out += ["0.000000", "0.000000", "1"]
        else:
            out += ["%.6f" % (canon(b) + 0.0), "%.6f" % (canon(c) + 0.0), "0"]
    else:
        return
    sys.stdout.write(" ".join(out) + "\n")


main()
