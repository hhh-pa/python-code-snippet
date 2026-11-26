# Multidimensional minimization by Powell's direction set
# method (with Brent line searches).
# Reference: Press et al., Numerical Recipes 3e, Sections 10.6-10.7.
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


def sgn(a, b):
    return abs(a) if b >= 0.0 else -abs(a)


class TooMany(Exception):
    pass


class Brent1:
    def __init__(self, ftol=3.0e-8):
        self.ftol = ftol

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


class Powell:
    def __init__(self, ftol):
        self.ftol = ftol
        self.fret = 0.0
        self.iter = 0
        self.p = []
        self.xi = []

    def linmin(self):
        n = len(self.p)
        p, xi = self.p, self.xi

        def f1dim(x):
            return func([p[j] + x * xi[j] for j in range(n)])

        br = Brent1()
        br.bracket(0.0, 1.0, f1dim)
        xmin = br.minimize(f1dim)
        for j in range(n):
            xi[j] *= xmin
            p[j] += xi[j]
        return br.fmin

    def minimize(self, pp):
        ITMAX = 200
        TINY = 1.0e-25
        n = len(pp)
        ximat = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        p = list(pp)
        self.p = p
        pt = list(p)
        ptt = [0.0] * n
        self.xi = [0.0] * n
        self.fret = func(p)
        it = 0
        while True:
            fp = self.fret
            ibig = 0
            dele = 0.0
            for i in range(n):
                for j in range(n):
                    self.xi[j] = ximat[j][i]
                fptt = self.fret
                self.fret = self.linmin()
                if fptt - self.fret > dele:
                    dele = fptt - self.fret
                    ibig = i + 1
            if 2.0 * (fp - self.fret) <= self.ftol * (abs(fp) + abs(self.fret)) + TINY:
                self.iter = it
                return p
            if it == ITMAX:
                self.iter = it
                raise TooMany()
            for j in range(n):
                ptt[j] = 2.0 * p[j] - pt[j]
                self.xi[j] = p[j] - pt[j]
                pt[j] = p[j]
            fptt = func(ptt)
            if fptt < fp:
                sq1 = fp - self.fret - dele
                sq1 *= sq1
                sq2 = fp - fptt
                sq2 *= sq2
                t = 2.0 * (fp - 2.0 * self.fret + fptt) * sq1 - dele * sq2
                if t < 0.0:
                    self.fret = self.linmin()
                    for j in range(n):
                        ximat[j][ibig - 1] = ximat[j][n - 1]
                        ximat[j][n - 1] = self.xi[j]
            it += 1


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
    if op == "POWELL":
        pw = Powell(ftol)
        try:
            pmin = pw.minimize(point)
            print(" ".join(fmt6(v) for v in pmin) + " %s %d 0" % (fmt6(pw.fret), pw.iter))
        except TooMany:
            print(" ".join(["0.000000"] * n) + " 0.000000 %d 1" % pw.iter)


main()
