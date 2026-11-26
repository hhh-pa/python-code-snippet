# Linear prediction: Burg LP coefficients (memcof), stabilization by
# root reflection (fixrts), and extrapolation (predic).
# Reference: Press et al., Numerical Recipes 3e, Section 13.7
# (memcof/fixrts/predic, vendoring zroots+laguer from 9.5 with the
# explicit real/imag complex flops of math/roots/poly_roots).
# Documented decisions: n >= 2 and 1 <= m < n are enforced (the
# book indexes out of bounds for n = 1 and divides 0/0 for
# m >= n); an exact-zero denom flags (the book yields NaN);
# PREDIC needs ndata >= m >= 1 (the book overruns or
# dereferences an empty register otherwise).
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys

MACEPS = 2.220446049250313e-16


class BadN(Exception):
    pass


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
    frac = [0.0, 0.5, 0.25, 0.75, 0.13, 0.38, 0.62, 0.88, 1.0]
    m = len(a) - 1
    for it in range(1, 81):
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
            return (0, x)
        g = cxdiv(d, b)
        g2 = cxmul(g, g)
        h = cxsub(g2, cxscale(cxdiv(f, b), 2.0))
        sq = cxsqrt(cxscale(cxsub(cxscale(h, float(m)), g2), float(m - 1)))
        gp = cxadd(g, sq)
        gm = cxsub(g, sq)
        abp = cxabs(gp)
        abm = cxabs(gm)
        if abp < abm:
            gp = gm
        mx = abm if abp < abm else abp
        if mx > 0.0:
            dx = cxdiv((float(m), 0.0), gp)
        else:
            dx = cxpolar(1 + abx, float(it))
        x1 = cxsub(x, dx)
        if x[0] == x1[0] and x[1] == x1[1]:
            return (0, x)
        if it % 10 != 0:
            x = x1
        else:
            x = cxsub(x, cxscale(dx, frac[it // 10]))
    return (1, x)


def zroots(a):
    EPS = 1.0e-14
    m = len(a) - 1
    ad = list(a)
    roots = [(0.0, 0.0)] * m
    for j in range(m - 1, -1, -1):
        x = (0.0, 0.0)
        flag, x = laguer(ad[:j + 2], x)
        if flag:
            return (1, roots)
        if abs(x[1]) <= 2.0 * EPS * abs(x[0]):
            x = (x[0], 0.0)
        roots[j] = x
        b = ad[j + 1]
        for jj in range(j, -1, -1):
            c = ad[jj]
            ad[jj] = b
            b = cxadd(cxmul(x, b), c)
    for j in range(m):
        flag, roots[j] = laguer(a, roots[j])
        if flag:
            return (1, roots)
    for j in range(1, m):
        x = roots[j]
        i = j - 1
        while i >= 0:
            if roots[i][0] <= x[0]:
                break
            roots[i + 1] = roots[i]
            i -= 1
        roots[i + 1] = x
    return (0, roots)


def memcof(data, m):
    n = len(data)
    if n < 2 or m < 1 or m >= n:
        raise BadN()
    d = [0.0] * m
    p = 0.0
    wk1 = [0.0] * n
    wk2 = [0.0] * n
    wkm = [0.0] * m
    for j in range(n):
        p += data[j] * data[j]
    xms = p / n
    wk1[0] = data[0]
    wk2[n - 2] = data[n - 1]
    for j in range(1, n - 1):
        wk1[j] = data[j]
        wk2[j - 1] = data[j]
    for k in range(m):
        num = 0.0
        denom = 0.0
        for j in range(n - k - 1):
            num += wk1[j] * wk2[j]
            denom += wk1[j] * wk1[j] + wk2[j] * wk2[j]
        if denom == 0.0:
            raise BadN()
        d[k] = 2.0 * num / denom
        t = d[k]
        xms *= 1.0 - t * t
        for i in range(k):
            d[i] = wkm[i] - d[k] * wkm[k - 1 - i]
        if k == m - 1:
            return (d, xms)
        for i in range(k + 1):
            wkm[i] = d[i]
        for j in range(n - k - 2):
            wk1[j] -= wkm[k] * wk2[j]
            wk2[j] = wk2[j + 1] - wkm[k] * wk1[j + 1]
    raise BadN()


def fixrts(d):
    m = len(d)
    if m < 1:
        raise BadN()
    a = [(0.0, 0.0)] * (m + 1)
    a[m] = (1.0, 0.0)
    for j in range(m):
        a[j] = (-d[m - 1 - j], 0.0)
    flag, roots = zroots(a)
    if flag:
        raise BadN()
    for j in range(m):
        if cxabs(roots[j]) > 1.0:
            c = (roots[j][0], -roots[j][1])
            roots[j] = cxdiv((1.0, 0.0), c)
    a[0] = (-roots[0][0], -roots[0][1])
    a[1] = (1.0, 0.0)
    for j in range(1, m):
        a[j + 1] = (1.0, 0.0)
        for i in range(j, 0, -1):
            a[i] = cxsub(a[i - 1], cxmul(roots[j], a[i]))
        a[0] = cxmul((-roots[j][0], -roots[j][1]), a[0])
    for j in range(m):
        d[m - 1 - j] = -a[j][0]
    return d


def predic(data, d, nfut):
    ndata = len(data)
    m = len(d)
    if ndata < m or m < 1:
        raise BadN()
    reg = [data[ndata - 1 - j] for j in range(m)]
    future = []
    for _ in range(nfut):
        s = 0.0
        for k in range(m):
            s += d[k] * reg[k]
        for k in range(m - 1, 0, -1):
            reg[k] = reg[k - 1]
        reg[0] = s
        future.append(s)
    return future


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "MEMCOF":
        n = int(toks[1])
        m = int(toks[2])
        data = [float(t) for t in toks[3:3 + max(0, n)]]
        try:
            d, xms = memcof(data, m)
            parts = [fmt6(v) for v in d]
            parts.append(fmt6(xms))
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * (m + 1)
            parts.append("1")
            print(" ".join(parts))
    elif op == "FIXRTS":
        m = int(toks[1])
        d = [float(t) for t in toks[2:2 + max(0, m)]]
        try:
            d = fixrts(d)
            parts = [fmt6(v) for v in d]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, m)
            parts.append("1")
            print(" ".join(parts))
    elif op == "PREDIC":
        ndata = int(toks[1])
        m = int(toks[2])
        nfut = int(toks[3])
        data = [float(t) for t in toks[4:4 + max(0, ndata)]]
        d = [float(t) for t in toks[4 + max(0, ndata):4 + max(0, ndata) + max(0, m)]]
        try:
            future = predic(data, d, nfut)
            parts = [fmt6(v) for v in future]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, nfut)
            parts.append("1")
            print(" ".join(parts))


main()
