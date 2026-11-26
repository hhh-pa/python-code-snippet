# Nonlinear systems (NR 9.6-9.7).
import math
import sys

SYS = ""
MACEPS = 2.220446049250313e-16


def vecfunc(x):
    if SYS == "SYS1":
        return [x[0] * x[0] + x[1] * x[1] - 4.0, x[0] * x[1] - 1.0]
    elif SYS == "SYS2":
        return [x[0] * x[0] - x[1] - 1.0, x[0] - x[1] * x[1] + 1.0]
    return [x[0] * x[0] + x[1] * x[1] + x[2] * x[2] - 14.0,
            x[0] * x[1] * x[2] - 6.0, x[0] + x[1] + x[2] - 6.0]


def jacfunc(x):
    n = len(x)
    j = [[0.0] * n for _ in range(n)]
    if SYS == "SYS1":
        j[0][0] = 2.0 * x[0]
        j[0][1] = 2.0 * x[1]
        j[1][0] = x[1]
        j[1][1] = x[0]
    elif SYS == "SYS2":
        j[0][0] = 2.0 * x[0]
        j[0][1] = -1.0
        j[1][0] = 1.0
        j[1][1] = -2.0 * x[1]
    else:
        j[0][0] = 2.0 * x[0]
        j[0][1] = 2.0 * x[1]
        j[0][2] = 2.0 * x[2]
        j[1][0] = x[1] * x[2]
        j[1][1] = x[0] * x[2]
        j[1][2] = x[0] * x[1]
        j[2][0] = 1.0
        j[2][1] = 1.0
        j[2][2] = 1.0
    return j


class Singular(Exception):
    pass


class LUdcmp:
    def __init__(self, a):
        n = len(a)
        self.n = n
        lu = [row[:] for row in a]
        self.lu = lu
        self.indx = [0] * n
        tiny = 1.0e-40
        vv = [0.0] * n
        for i in range(n):
            big = 0.0
            for j in range(n):
                temp = abs(lu[i][j])
                if temp > big:
                    big = temp
            if big == 0.0:
                raise Singular()
            vv[i] = 1.0 / big
        for k in range(n):
            big = 0.0
            imax = k
            for i in range(k, n):
                temp = vv[i] * abs(lu[i][k])
                if temp > big:
                    big = temp
                    imax = i
            if k != imax:
                lu[k], lu[imax] = lu[imax], lu[k]
                vv[imax] = vv[k]
            self.indx[k] = imax
            if lu[k][k] == 0.0:
                lu[k][k] = tiny
            for i in range(k + 1, n):
                temp = lu[i][k] / lu[k][k]
                lu[i][k] = temp
                for j in range(k + 1, n):
                    lu[i][j] -= temp * lu[k][j]

    def solve(self, b):
        n = self.n
        lu = self.lu
        x = list(b)
        ii = 0
        for i in range(n):
            ip = self.indx[i]
            sm = x[ip]
            x[ip] = x[i]
            if ii != 0:
                for j in range(ii - 1, i):
                    sm -= lu[i][j] * x[j]
            elif sm != 0.0:
                ii = i + 1
            x[i] = sm
        for i in range(n - 1, -1, -1):
            sm = x[i]
            for j in range(i + 1, n):
                sm -= lu[i][j] * x[j]
            x[i] = sm / lu[i][i]
        return x


class QRdcmp:
    def __init__(self, a):
        n = len(a)
        self.n = n
        self.sing = False
        qt = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        r = [row[:] for row in a]
        c = [0.0] * n
        d = [0.0] * n
        for k in range(n - 1):
            scale = 0.0
            for i in range(k, n):
                scale = max(scale, abs(r[i][k]))
            if scale == 0.0:
                self.sing = True
                c[k] = d[k] = 0.0
            else:
                for i in range(k, n):
                    r[i][k] /= scale
                sm = 0.0
                for i in range(k, n):
                    sm += r[i][k] * r[i][k]
                sigma = math.sqrt(sm) if r[k][k] >= 0.0 else -math.sqrt(sm)
                r[k][k] += sigma
                c[k] = sigma * r[k][k]
                d[k] = -scale * sigma
                for j in range(k + 1, n):
                    s = 0.0
                    for i in range(k, n):
                        s += r[i][k] * r[i][j]
                    tau = s / c[k]
                    for i in range(k, n):
                        r[i][j] -= tau * r[i][k]
        d[n - 1] = r[n - 1][n - 1]
        if d[n - 1] == 0.0:
            self.sing = True
        for k in range(n - 1):
            if c[k] != 0.0:
                for j in range(n):
                    sm = 0.0
                    for i in range(k, n):
                        sm += r[i][k] * qt[i][j]
                    sm /= c[k]
                    for i in range(k, n):
                        qt[i][j] -= sm * r[i][k]
        for i in range(n):
            r[i][i] = d[i]
            for j in range(i):
                r[i][j] = 0.0
        self.qt = qt
        self.r = r

    def rotate(self, i, a, b):
        n = self.n
        r, qt = self.r, self.qt
        if a == 0.0:
            cc = 0.0
            s = 1.0 if b >= 0.0 else -1.0
        elif abs(a) > abs(b):
            fact = b / a
            cc = 1.0 / math.sqrt(1.0 + fact * fact)
            cc = cc if a >= 0.0 else -cc
            s = fact * cc
        else:
            fact = a / b
            s = 1.0 / math.sqrt(1.0 + fact * fact)
            s = s if b >= 0.0 else -s
            cc = fact * s
        for j in range(i, n):
            y = r[i][j]
            w = r[i + 1][j]
            r[i][j] = cc * y - s * w
            r[i + 1][j] = s * y + cc * w
        for j in range(n):
            y = qt[i][j]
            w = qt[i + 1][j]
            qt[i][j] = cc * y - s * w
            qt[i + 1][j] = s * y + cc * w

    def qtmult(self, b):
        n = self.n
        return [sum(self.qt[i][j] * b[j] for j in range(n)) for i in range(n)]

    def rsolve(self, b):
        n = self.n
        x = list(b)
        for i in range(n - 1, -1, -1):
            sm = x[i]
            for j in range(i + 1, n):
                sm -= self.r[i][j] * x[j]
            x[i] = sm / self.r[i][i]
        return x

    def update(self, u, v):
        n = self.n
        r = self.r
        w = list(u)
        k = n - 1
        while k >= 0 and w[k] == 0.0:
            k -= 1
        if k < 0:
            k = 0
        for i in range(k - 1, -1, -1):
            self.rotate(i, w[i], -w[i + 1])
            if w[i] == 0.0:
                w[i] = abs(w[i + 1])
            elif abs(w[i]) > abs(w[i + 1]):
                w[i] = abs(w[i]) * math.sqrt(1.0 + (w[i + 1] / w[i]) ** 2)
            else:
                w[i] = abs(w[i + 1]) * math.sqrt(1.0 + (w[i] / w[i + 1]) ** 2)
        for i in range(n):
            r[0][i] += w[0] * v[i]
        for i in range(k):
            self.rotate(i, r[i][i], -r[i + 1][i])
        for i in range(n):
            if r[i][i] == 0.0:
                self.sing = True


def fdjac(x, fvec):
    eps = 1.0e-8
    n = len(x)
    df = [[0.0] * n for _ in range(n)]
    xh = list(x)
    for j in range(n):
        temp = xh[j]
        h = eps * abs(temp)
        if h == 0.0:
            h = eps
        xh[j] = temp + h
        h = xh[j] - temp
        f = vecfunc(xh)
        xh[j] = temp
        for i in range(n):
            df[i][j] = (f[i] - fvec[i]) / h
    return df


def fminfn(x):
    fvec = vecfunc(x)
    return 0.5 * sum(v * v for v in fvec), fvec


def mnewt(x, ntrial, tolx, tolf):
    n = len(x)
    for _ in range(ntrial):
        fvec = vecfunc(x)
        fjac = jacfunc(x)
        if sum(abs(v) for v in fvec) <= tolf:
            return
        p = [-v for v in fvec]
        alu = LUdcmp(fjac)
        p = alu.solve(p)
        errx = sum(abs(v) for v in p)
        x[:] = [a + b for a, b in zip(x, p)]
        if errx <= tolx:
            return


def lnsrch(xold, fold, g, p, stpmax):
    alf = 1.0e-4
    tolx = MACEPS
    n = len(xold)
    check = False
    sm = math.sqrt(sum(v * v for v in p))
    if sm > stpmax:
        p = [v * stpmax / sm for v in p]
    slope = sum(a * b for a, b in zip(g, p))
    if slope >= 0.0:
        return None, 0.0, True, True
    test = 0.0
    for i in range(n):
        temp = abs(p[i]) / max(abs(xold[i]), 1.0)
        if temp > test:
            test = temp
    alamin = tolx / test
    alam = 1.0
    alam2, f2 = 0.0, 0.0
    while True:
        x = [a + alam * b for a, b in zip(xold, p)]
        f, _ = fminfn(x)
        if alam < alamin:
            return list(xold), f, True, False
        elif f <= fold + alf * alam * slope:
            return x, f, False, False
        if alam == 1.0:
            tmplam = -slope / (2.0 * (f - fold - slope))
        else:
            rhs1 = f - fold - alam * slope
            rhs2 = f2 - fold - alam2 * slope
            a = (rhs1 / (alam * alam) - rhs2 / (alam2 * alam2)) / (alam - alam2)
            b = (-alam2 * rhs1 / (alam * alam) + alam * rhs2 / (alam2 * alam2)) / (alam - alam2)
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
        alam2, f2 = alam, f
        alam = max(tmplam, 0.1 * alam)


def newt(x):
    maxits, tolf, tolmin, stpmx = 200, 1.0e-8, 1.0e-12, 100.0
    tolx = MACEPS
    n = len(x)
    f, fvec = fminfn(x)
    if max(abs(v) for v in fvec) < 0.01 * tolf:
        return x, False, 0
    stpmax = stpmx * max(math.sqrt(sum(v * v for v in x)), float(n))
    for _ in range(maxits):
        fjac = fdjac(x, fvec)
        g = [sum(fjac[j][i] * fvec[j] for j in range(n)) for i in range(n)]
        xold = list(x)
        fold = f
        p = [-v for v in fvec]
        try:
            alu = LUdcmp(fjac)
            p = alu.solve(p)
        except Singular:
            return x, False, 1
        x, f, check, bad = lnsrch(xold, fold, g, p, stpmax)
        if bad:
            return x, False, 1
        fvec = vecfunc(x)
        if max(abs(v) for v in fvec) < tolf:
            return x, False, 0
        if check:
            den = max(f, 0.5 * n)
            test = 0.0
            for i in range(n):
                temp = abs(g[i]) * max(abs(x[i]), 1.0) / den
                if temp > test:
                    test = temp
            return x, (test < tolmin), 0
        test = 0.0
        for i in range(n):
            temp = abs(x[i] - xold[i]) / max(abs(x[i]), 1.0)
            if temp > test:
                test = temp
        if test < tolx:
            return x, False, 0
    return x, False, 1


def broydn(x):
    maxits, tolf, tolx, stpmx, tolmin = 200, 1.0e-8, MACEPS, 100.0, 1.0e-12
    n = len(x)
    f, fvec = fminfn(x)
    if max(abs(v) for v in fvec) < 0.01 * tolf:
        return x, False, 0
    stpmax = stpmx * max(math.sqrt(sum(v * v for v in x)), float(n))
    restrt = True
    for _ in range(1, maxits + 1):
        if restrt:
            qr = QRdcmp(fdjac(x, fvec))
            if qr.sing:
                return x, False, 1
        else:
            s = [a - b for a, b in zip(x, xold)]
            t = [sum(qr.r[i][j] * s[j] for j in range(i, n)) for i in range(n)]
            skip = True
            w = [0.0] * n
            for i in range(n):
                sm = sum(qr.qt[j][i] * t[j] for j in range(n))
                w[i] = fvec[i] - fvcold[i] - sm
                if abs(w[i]) >= MACEPS * (abs(fvec[i]) + abs(fvcold[i])):
                    skip = False
                else:
                    w[i] = 0.0
            if not skip:
                t = qr.qtmult(w)
                den = sum(v * v for v in s)
                s = [v / den for v in s]
                qr.update(t, s)
                if qr.sing:
                    return x, False, 1
        p = [-v for v in qr.qtmult(fvec)]
        g = [0.0] * n
        for i in range(n - 1, -1, -1):
            s = 0.0
            for j in range(i + 1):
                s -= qr.r[j][i] * p[j]
            g[i] = s
        xold = list(x)
        fvcold = list(fvec)
        fold = f
        p = qr.rsolve(p)
        x, f, check, bad = lnsrch(xold, fold, g, p, stpmax)
        if bad:
            return x, False, 1
        fvec = vecfunc(x)
        if max(abs(v) for v in fvec) < tolf:
            return x, False, 0
        if check:
            if restrt:
                return x, True, 0
            den = max(f, 0.5 * n)
            test = 0.0
            for i in range(n):
                temp = abs(g[i]) * max(abs(x[i]), 1.0) / den
                if temp > test:
                    test = temp
            if test < tolmin:
                return x, True, 0
            restrt = True
        else:
            restrt = False
            test = 0.0
            for i in range(n):
                temp = abs(x[i] - xold[i]) / max(abs(x[i]), 1.0)
                if temp > test:
                    test = temp
            if test < tolx:
                return x, False, 0
    return x, False, 1


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    global SYS
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    SYS = toks[1]
    n = 3 if SYS == "SYS3" else 2
    x = [float(w) for w in toks[2:2 + n]]
    p = 2 + n
    out = []
    if op == "MNEWT":
        ntrial, tolx, tolf = int(toks[p]), float(toks[p + 1]), float(toks[p + 2])
        try:
            mnewt(x, ntrial, tolx, tolf)
            out = ["%.6f" % (canon(v) + 0.0) for v in x] + ["0"]
        except Singular:
            out = ["0.000000"] * n + ["1"]
    elif op in ("NEWT", "BROYDN"):
        x, check, flag = newt(x) if op == "NEWT" else broydn(x)
        vals = [0.0] * n if flag else x
        out = ["%.6f" % (canon(v) + 0.0) for v in vals] + [str(int(check)), str(flag)]
    elif op == "LNSRCH":
        pv = [float(w) for w in toks[p:p + n]]
        stpmax = float(toks[p + n])
        fvec = vecfunc(x)
        fold = 0.5 * sum(v * v for v in fvec)
        fj = fdjac(x, fvec)
        g = [sum(fj[j][i] * fvec[j] for j in range(n)) for i in range(n)]
        xn, f, check, bad = lnsrch(x, fold, g, pv, stpmax)
        if bad:
            out = ["%.6f" % (canon(v) + 0.0) for v in x] + \
                ["%.6f" % (canon(fold) + 0.0), "1"]
        else:
            out = ["%.6f" % (canon(v) + 0.0) for v in xn] + \
                ["%.6f" % (canon(f) + 0.0), str(int(check))]
    else:
        return
    sys.stdout.write(" ".join(out) + "\n")


main()
