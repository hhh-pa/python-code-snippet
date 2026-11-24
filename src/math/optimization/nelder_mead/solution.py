# Multidimensional minimization by the downhill simplex
# method of Nelder and Mead (Amoeba).
# Reference: Press et al., Numerical Recipes 3e, Section 10.5.
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


class TooMany(Exception):
    pass


class Amoeba:
    def __init__(self, ftol):
        self.ftol = ftol
        self.nfunc = 0
        self.fmin = 0.0

    def minimize_pt(self, point, dele):
        n = len(point)
        pp = [list(point) for _ in range(n + 1)]
        for i in range(1, n + 1):
            pp[i][i - 1] += dele
        return self.minimize(pp)

    def minimize(self, pp):
        NMAX = 5000
        TINY = 1.0e-10
        mpts = len(pp)
        ndim = len(pp[0])
        p = [list(row) for row in pp]
        y = [0.0] * mpts
        for i in range(mpts):
            y[i] = func(p[i])
        self.nfunc = 0
        psum = [0.0] * ndim
        self.get_psum(p, psum, mpts, ndim)
        while True:
            ilo = 0
            if y[0] > y[1]:
                inhi = 1
                ihi = 0
            else:
                inhi = 0
                ihi = 1
            for i in range(mpts):
                if y[i] <= y[ilo]:
                    ilo = i
                if y[i] > y[ihi]:
                    inhi = ihi
                    ihi = i
                elif y[i] > y[inhi] and i != ihi:
                    inhi = i
            rtol = 2.0 * abs(y[ihi] - y[ilo]) / (abs(y[ihi]) + abs(y[ilo]) + TINY)
            if rtol < self.ftol:
                y[0], y[ilo] = y[ilo], y[0]
                pmin = [0.0] * ndim
                for i in range(ndim):
                    p[0][i], p[ilo][i] = p[ilo][i], p[0][i]
                    pmin[i] = p[0][i]
                self.fmin = y[0]
                return pmin
            if self.nfunc >= NMAX:
                raise TooMany()
            self.nfunc += 2
            ytry = self.amotry(p, y, psum, ihi, -1.0, ndim)
            if ytry <= y[ilo]:
                ytry = self.amotry(p, y, psum, ihi, 2.0, ndim)
            elif ytry >= y[inhi]:
                ysave = y[ihi]
                ytry = self.amotry(p, y, psum, ihi, 0.5, ndim)
                if ytry >= ysave:
                    for i in range(mpts):
                        if i != ilo:
                            for j in range(ndim):
                                v = 0.5 * (p[i][j] + p[ilo][j])
                                p[i][j] = v
                                psum[j] = v
                            y[i] = func(psum)
                    self.nfunc += ndim
                    self.get_psum(p, psum, mpts, ndim)
            else:
                self.nfunc -= 1

    def get_psum(self, p, psum, mpts, ndim):
        for j in range(ndim):
            s = 0.0
            for i in range(mpts):
                s += p[i][j]
            psum[j] = s

    def amotry(self, p, y, psum, ihi, fac, ndim):
        fac1 = (1.0 - fac) / ndim
        fac2 = fac1 - fac
        ptry = [psum[j] * fac1 - p[ihi][j] * fac2 for j in range(ndim)]
        ytry = func(ptry)
        if ytry < y[ihi]:
            y[ihi] = ytry
            for j in range(ndim):
                psum[j] += ptry[j] - p[ihi][j]
                p[ihi][j] = ptry[j]
        return ytry


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
    dele = float(toks[p])
    ftol = float(toks[p + 1])
    if op == "AMOEBA":
        am = Amoeba(ftol)
        try:
            pmin = am.minimize_pt(point, dele)
            print(" ".join(fmt6(v) for v in pmin) + " %s %d 0" % (fmt6(am.fmin), am.nfunc))
        except TooMany:
            print(" ".join(["0.000000"] * n) + " 0.000000 %d 1" % am.nfunc)


main()
