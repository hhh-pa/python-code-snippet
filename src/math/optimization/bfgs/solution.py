# Multidimensional minimization by the Broyden-Fletcher-
# Goldfarb-Shanno quasi-Newton method (NR dfpmin, BFGS
# updating, lnsrch backtracking line searches).
# Reference: Press et al., Numerical Recipes 3e, Section 10.9.
# No online-judge problem found -- fixtures are self-generated
# (scipy oracle), no header link.
import math
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


class TooMany(Exception):
    pass


def lnsrch(xold, fold, g, p, x, stpmax, f_in):
    ALF = 1.0e-4
    TOLX = 2.220446049250313e-16
    n = len(xold)
    check = False
    s = 0.0
    for i in range(n):
        s += p[i] * p[i]
    s = math.sqrt(s)
    if s > stpmax:
        for i in range(n):
            p[i] *= stpmax / s
    slope = 0.0
    for i in range(n):
        slope += g[i] * p[i]
    if slope >= 0.0:
        return f_in, check, 1
    test = 0.0
    for i in range(n):
        temp = abs(p[i]) / max(abs(xold[i]), 1.0)
        if temp > test:
            test = temp
    alamin = TOLX / test
    alam = 1.0
    alam2 = 0.0
    f2 = 0.0
    while True:
        for i in range(n):
            x[i] = xold[i] + alam * p[i]
        f = func(x)
        if alam < alamin:
            for i in range(n):
                x[i] = xold[i]
            check = True
            return f, check, 0
        elif f <= fold + ALF * alam * slope:
            return f, check, 0
        else:
            if alam == 1.0:
                tmplam = -slope / (2.0 * (f - fold - slope))
            else:
                rhs1 = f - fold - alam * slope
                rhs2 = f2 - fold - alam2 * slope
                a = (rhs1 / (alam * alam) - rhs2 / (alam2 * alam2)) / (alam - alam2)
                b = (-alam2 * rhs1 / (alam * alam) + alam * rhs2 / (alam2 * alam2)) / (
                    alam - alam2)
                if a == 0.0:
                    tmplam = -slope / (2.0 * b)
                else:
                    disc = b * b - 3.0 * a * slope
                    if disc < 0.0:
                        tmplam = 0.5 * alam
                    elif b <= 0.0:
                        tmplam = (-b + math.sqrt(disc)) / (3.0 * a)
                    else:
                        tmplam = -slope / (b + math.sqrt(disc))
                if tmplam > 0.5 * alam:
                    tmplam = 0.5 * alam
        alam2 = alam
        f2 = f
        alam = max(tmplam, 0.1 * alam)


class Bfgs:
    def __init__(self, gtol):
        self.gtol = gtol
        self.fret = 0.0
        self.iter = 0

    def minimize(self, pp):
        ITMAX = 200
        EPS = 2.220446049250313e-16
        TOLX = 4 * EPS
        STPMX = 100.0
        n = len(pp)
        p = list(pp)
        dg = [0.0] * n
        g = [0.0] * n
        hdg = [0.0] * n
        pnew = [0.0] * n
        xi = [0.0] * n
        hessin = [[0.0] * n for _ in range(n)]
        fp = func(p)
        df = funcdf(p)
        s = 0.0
        for i in range(n):
            for j in range(n):
                hessin[i][j] = 0.0
            hessin[i][i] = 1.0
            g[i] = df[i]
            xi[i] = -g[i]
            s += p[i] * p[i]
        stpmax = STPMX * max(math.sqrt(s), float(n))
        for its in range(ITMAX):
            self.iter = its
            pnew = list(p)
            f, check, bad = lnsrch(p, fp, g, xi, pnew, stpmax, self.fret)
            self.fret = f
            fp = self.fret
            for i in range(n):
                xi[i] = pnew[i] - p[i]
                p[i] = pnew[i]
            test = 0.0
            for i in range(n):
                temp = abs(xi[i]) / max(abs(p[i]), 1.0)
                if temp > test:
                    test = temp
            if test < TOLX:
                return p
            for i in range(n):
                dg[i] = g[i]
            df = funcdf(p)
            for i in range(n):
                g[i] = df[i]
            test = 0.0
            den = max(self.fret, 1.0)
            for i in range(n):
                temp = abs(g[i]) * max(abs(p[i]), 1.0) / den
                if temp > test:
                    test = temp
            if test < self.gtol:
                return p
            for i in range(n):
                dg[i] = g[i] - dg[i]
            for i in range(n):
                hdg[i] = 0.0
                for j in range(n):
                    hdg[i] += hessin[i][j] * dg[j]
            fac = 0.0
            fae = 0.0
            sumdg = 0.0
            sumxi = 0.0
            for i in range(n):
                fac += dg[i] * xi[i]
                fae += dg[i] * hdg[i]
                sumdg += dg[i] * dg[i]
                sumxi += xi[i] * xi[i]
            if fac > math.sqrt(EPS * sumdg * sumxi):
                fac = 1.0 / fac
                fad = 1.0 / fae
                for i in range(n):
                    dg[i] = fac * xi[i] - fad * hdg[i]
                for i in range(n):
                    for j in range(i, n):
                        hessin[i][j] += fac * xi[i] * xi[j] - fad * hdg[i] * hdg[j] + fae * dg[
                            i] * dg[j]
                        hessin[j][i] = hessin[i][j]
            for i in range(n):
                xi[i] = 0.0
                for j in range(n):
                    xi[i] -= hessin[i][j] * g[j]
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
    gtol = float(toks[p])
    if op == "BFGS":
        bf = Bfgs(gtol)
        try:
            pmin = bf.minimize(point)
            print(" ".join(fmt6(v) for v in pmin) + " %s %d 0" % (fmt6(bf.fret), bf.iter))
        except TooMany:
            print(" ".join(["0.000000"] * n) + " 0.000000 %d 1" % bf.iter)


main()
