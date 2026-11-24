# Laplace interpolation (NR 3.8).
import sys


def fmt6(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    it = iter(toks)
    nx = int(next(it))
    ny = int(next(it))
    x0 = float(next(it))
    x1 = float(next(it))
    y0 = float(next(it))
    y1 = float(next(it))
    k = int(next(it))
    px, py, pz = [], [], []
    for _ in range(k):
        px.append(float(next(it)))
        py.append(float(next(it)))
        pz.append(float(next(it)))
    dx = (x1 - x0) / (nx - 1)
    dy = (y1 - y0) / (ny - 1)
    ci, cj, w = [], [], []
    for p in range(k):
        fx = (px[p] - x0) / dx
        fy = (py[p] - y0) / dy
        if fx < 0:
            fx = 0.0
        if fy < 0:
            fy = 0.0
        if fx > nx - 1:
            fx = float(nx - 1)
        if fy > ny - 1:
            fy = float(ny - 1)
        i = int(fx)
        j = int(fy)
        if i > nx - 2:
            i = nx - 2
        if j > ny - 2:
            j = ny - 2
        tx = fx - i
        ty = fy - j
        if tx < 0:
            tx = 0.0
        if ty < 0:
            ty = 0.0
        if tx > 1:
            tx = 1.0
        if ty > 1:
            ty = 1.0
        ci.append(i)
        cj.append(j)
        w.append([(1 - tx) * (1 - ty), tx * (1 - ty),
                  (1 - tx) * ty, tx * ty])
    ng = nx * ny
    n = ng + k

    def idx(i, j):
        return i * ny + j

    diag = [0.0] * n
    for i in range(nx):
        for j in range(ny):
            d = 0
            if i > 0:
                d += 1
            if i < nx - 1:
                d += 1
            if j > 0:
                d += 1
            if j < ny - 1:
                d += 1
            diag[idx(i, j)] = float(d)
    for p in range(k):
        diag[ng + p] = 1.0

    def matvec(x, y):
        for t in range(n):
            y[t] = 0.0
        for i in range(nx):
            for j in range(ny):
                s = diag[idx(i, j)] * x[idx(i, j)]
                if i > 0:
                    s -= x[idx(i - 1, j)]
                if i < nx - 1:
                    s -= x[idx(i + 1, j)]
                if j > 0:
                    s -= x[idx(i, j - 1)]
                if j < ny - 1:
                    s -= x[idx(i, j + 1)]
                y[idx(i, j)] = s
        for p in range(k):
            i = ci[p]
            j = cj[p]
            lam = x[ng + p]
            y[idx(i, j)] += w[p][0] * lam
            y[idx(i + 1, j)] += w[p][1] * lam
            y[idx(i, j + 1)] += w[p][2] * lam
            y[idx(i + 1, j + 1)] += w[p][3] * lam
            y[ng + p] = (w[p][0] * x[idx(i, j)] +
                          w[p][1] * x[idx(i + 1, j)] +
                          w[p][2] * x[idx(i, j + 1)] +
                          w[p][3] * x[idx(i + 1, j + 1)])

    def dot(a, b):
        s = 0.0
        for t in range(n):
            s += a[t] * b[t]
        return s

    x = [0.0] * n
    r = [0.0] * n
    rt = [0.0] * n
    pp = [0.0] * n
    pt = [0.0] * n
    z = [0.0] * n
    zt = [0.0] * n
    q = [0.0] * n
    qt = [0.0] * n
    for p in range(k):
        x[ng + p] = pz[p]
    matvec(x, q)
    for i in range(n):
        b = 0.0 if i < ng else pz[i - ng]
        r[i] = b - q[i]
    rt = list(r)
    rho = 1.0
    for _ in range(400):
        for i in range(n):
            z[i] = r[i] / diag[i]
            zt[i] = rt[i] / diag[i]
        rhon = dot(rt, z)
        beta = 0.0 if rho == 0.0 else rhon / rho
        for i in range(n):
            pp[i] = z[i] + beta * pp[i]
            pt[i] = zt[i] + beta * pt[i]
        matvec(pp, q)
        matvec(pt, qt)
        sig = dot(pt, q)
        alpha = 0.0 if sig == 0.0 else rhon / sig
        for i in range(n):
            x[i] += alpha * pp[i]
            r[i] -= alpha * q[i]
            rt[i] -= alpha * qt[i]
        rho = rhon
    lines = []
    for i in range(nx):
        lines.append(" ".join(fmt6(x[idx(i, j)]) for j in range(ny)))
    sys.stdout.write("\n".join(lines) + "\n")


main()
