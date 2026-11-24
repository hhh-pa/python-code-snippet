# Multidimensional minimization by the Fletcher-Reeves and
# Polak-Ribiere conjugate gradient methods (with Brent line
# searches).
# Reference: Press et al., Numerical Recipes 3e, Section 10.8.
# No online-judge problem found -- fixtures are self-generated
# (scipy oracle), no header link.
import sys

fn = ""
fp = []


def func(x):
    if fn == "QUAD":
        n = len(x)
        s = fp[n]
        for i in range(n):
            s += (x[i] - fp[i]) * (x[i] - fp[i])
        return s
    else:
        n = len(x)
        s = 0.0
        for i in range(n - 1):
            a = x[i + 1] - x[i] * x[i]
            b = 1.0 - x[i]
            s += 100.0 * a * a + b * b
        return s


def funcdf(x):
    n = len(x)
    df = [0.0] * n
    if fn == "QUAD":
        for i in range(n):
            df[i] = 2.0 * (x[i] - fp[i])
    else:
        df[0] = -400.0 * x[0] * (x[1] - x[0] * x[0]) - 2.0 * (1.0 - x[0])
        for i in range(1, n - 1):
            df[i] = 200.0 * (x[i] - x[i - 1] * x[i - 1]) - 400.0 * x[i] * (
                x[i + 1] - x[i] * x[i]) - 2.0 * (1.0 - x[i])
        df[n - 1] = 200.0 * (x[n - 1] - x[n - 2] * x[n - 2])
    return df


def sgn(a, b):
    return abs(a) if b >= 0.0 else -abs(a)


class TooMany(Exception):
    pass


class Brent1:
    def __init__(self, ftol=3.0e-8):
        self.ftol = ftol
        self.fmin = 0.0

    def bracket(self, a, b, f):
        GOLD = 1.618034
        GLIMIT = 100.0
        TINY = 1.0e-20
        ax, bx = a, b
        fa, fb = f(ax), f(bx)
        if fb > fa:
            ax, bx = bx, ax
            fa, fb = fb, fa
        cx = bx + GOLD * (bx - ax)
        fc = f(cx)
        while fb > fc:
            r = (bx - ax) * (fb - fc)
            q = (bx - cx) * (fb - fa)
            u = bx - ((bx - cx) * q - (bx - ax) * r) / (
                2.0 * sgn(max(abs(q - r), TINY), q - r))
            ulim = bx + GLIMIT * (cx - bx)
            if (bx - u) * (u - cx) > 0.0:
                fu = f(u)
                if fu < fc:
                    ax, bx, fa, fb = bx, u, fb, fu
                    break
                elif fu > fb:
                    cx, fc = u, fu
                    break
                u = cx + GOLD * (cx - bx)
                fu = f(u)
            elif (cx - u) * (u - ulim) > 0.0:
                fu = f(u)
                if fu < fc:
                    nu = u + GOLD * (u - cx)
                    nfu = f(nu)
                    bx, cx, u = cx, u, nu
                    fb, fc, fu = fc, fu, nfu
            elif (u - ulim) * (ulim - cx) >= 0.0:
                u = ulim
                fu = f(u)
            else:
                u = cx + GOLD * (cx - bx)
                fu = f(u)
            ax, bx, cx = bx, cx, u
            fa, fb, fc = fb, fc, fu
        self.ax, self.bx, self.cx = ax, bx, cx

    def minimize(self, f):
        ITMAX = 100
        CGOLD = 0.3819660
        ZEPS = 2.220446049250313e-16 * 1.0e-3
        d = 0.0
        e = 0.0
        a = self.ax if self.ax < self.cx else self.cx
        b = self.ax if self.ax > self.cx else self.cx
        x = w = v = self.bx
        fw = fv = fx = f(x)
        for _ in range(ITMAX):
            xm = 0.5 * (a + b)
            tol1 = self.ftol * abs(x) + ZEPS
            tol2 = 2.0 * tol1
            if abs(x - xm) <= (tol2 - 0.5 * (b - a)):
                self.fmin = fx
                return x
            if abs(e) > tol1:
                r = (x - w) * (fx - fv)
                q0 = (x - v) * (fx - fw)
                p = (x - v) * q0 - (x - w) * r
                q = 2.0 * (q0 - r)
                if q > 0.0:
                    p = -p
                q = abs(q)
                etemp = e
                e = d
                if abs(p) >= abs(0.5 * q * etemp) or p <= q * (a - x) or p >= q * (b - x):
                    e = a - x if x >= xm else b - x
                    d = CGOLD * e
                else:
                    d = p / q
                    u = x + d
                    if u - a < tol2 or b - u < tol2:
                        d = sgn(tol1, xm - x)
            else:
                e = a - x if x >= xm else b - x
                d = CGOLD * e
            u = x + d if abs(d) >= tol1 else x + sgn(tol1, d)
            fu = f(u)
            if fu <= fx:
                if u >= x:
                    a = x
                else:
                    b = x
                v, w, x = w, x, u
                fv, fw, fx = fw, fx, fu
            else:
                if u < x:
                    a = u
                else:
                    b = u
                if fu <= fw or w == x:
                    v, w, fv, fw = w, u, fw, fu
                elif fu <= fv or v == x or v == w:
                    v, fv = u, fu
        raise TooMany()


class Frprmn:
    def __init__(self, ftol, use_pr):
        self.ftol = ftol
        self.use_pr = use_pr
        self.fret = 0.0
        self.iter = 0
        self.p = []
        self.xi = []

    def linmin(self):
        n = len(self.p)
        p = list(self.p)
        xi = list(self.xi)

        def f1dim(x):
            return func([p[j] + x * xi[j] for j in range(n)])

        br = Brent1()
        br.bracket(0.0, 1.0, f1dim)
        xmin = br.minimize(f1dim)
        for j in range(n):
            self.xi[j] *= xmin
            self.p[j] += self.xi[j]
        return br.fmin

    def minimize(self, pp):
        ITMAX = 200
        EPS = 1.0e-18
        GTOL = 1.0e-8
        n = len(pp)
        p = list(pp)
        self.p = p
        g = [0.0] * n
        h = [0.0] * n
        self.xi = [0.0] * n
        fp = func(p)
        df = funcdf(p)
        for j in range(n):
            g[j] = -df[j]
            self.xi[j] = g[j]
            h[j] = g[j]
        for its in range(ITMAX):
            self.iter = its
            self.fret = self.linmin()
            if 2.0 * abs(self.fret - fp) <= self.ftol * (abs(self.fret) + abs(fp) + EPS):
                return p
            fp = self.fret
            df = funcdf(p)
            for j in range(n):
                self.xi[j] = df[j]
            test = 0.0
            den = max(fp, 1.0)
            for j in range(n):
                temp = abs(self.xi[j]) * max(abs(p[j]), 1.0) / den
                if temp > test:
                    test = temp
            if test < GTOL:
                return p
            gg = 0.0
            dgg = 0.0
            for j in range(n):
                gg += g[j] * g[j]
                if self.use_pr:
                    dgg += (self.xi[j] + g[j]) * self.xi[j]
                else:
                    dgg += self.xi[j] * self.xi[j]
            if gg == 0.0:
                return p
            gam = dgg / gg
            for j in range(n):
                g[j] = -self.xi[j]
                self.xi[j] = g[j] + gam * h[j]
                h[j] = self.xi[j]
        raise TooMany()


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def main():
    global fn, fp
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    fn = toks[1]
    p = 2
    if fn == "QUAD":
        n = int(toks[p])
        p += 1
        fp = [float(toks[p + i]) for i in range(n + 1)]
        p += n + 1
    else:
        n = int(toks[p])
        p += 1
        fp = []
    point = [float(toks[p + i]) for i in range(n)]
    p += n
    ftol = float(toks[p])
    if op == "FR" or op == "PR":
        cg = Frprmn(ftol, op == "PR")
        try:
            pmin = cg.minimize(point)
            print(" ".join(fmt6(v) for v in pmin) + " %s %d 0" % (fmt6(cg.fret), cg.iter))
        except TooMany:
            print(" ".join(["0.000000"] * n) + " 0.000000 %d 1" % cg.iter)


main()
