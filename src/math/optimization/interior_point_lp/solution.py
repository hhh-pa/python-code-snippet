# Linear programming by the book's basic primal-dual
# infeasible interior-point method (routine intpt; dense
# LU substitutes the book's external sparse LDL+AMD
# backend, a Webnote-only performance optimization).
# Reference: Press et al., Numerical Recipes 3e, Section 10.11.
# No online-judge problem found -- fixtures are self-generated
# (scipy oracle), no header link.
import math
import sys


def dotprod(x, y):
    s = 0.0
    for i in range(len(x)):
        s += x[i] * y[i]
    return s


class Singular(Exception):
    pass


class LUdcmp:
    def __init__(self, a):
        n = len(a)
        self.n = n
        self.lu = [list(row) for row in a]
        self.indx = [0] * n
        TINY = 1.0e-40
        vv = [0.0] * n
        for i in range(n):
            big = 0.0
            for j in range(n):
                temp = abs(self.lu[i][j])
                if temp > big:
                    big = temp
            if big == 0.0:
                raise Singular()
            vv[i] = 1.0 / big
        for k in range(n):
            big = 0.0
            imax = k
            for i in range(k, n):
                temp = vv[i] * abs(self.lu[i][k])
                if temp > big:
                    big = temp
                    imax = i
            if k != imax:
                for j in range(n):
                    tmp = self.lu[imax][j]
                    self.lu[imax][j] = self.lu[k][j]
                    self.lu[k][j] = tmp
                vv[imax] = vv[k]
            self.indx[k] = imax
            if self.lu[k][k] == 0.0:
                self.lu[k][k] = TINY
            for i in range(k + 1, n):
                self.lu[i][k] /= self.lu[k][k]
                temp = self.lu[i][k]
                for j in range(k + 1, n):
                    self.lu[i][j] -= temp * self.lu[k][j]

    def solve(self, b, x):
        n = self.n
        for i in range(n):
            x[i] = b[i]
        ii = 0
        for i in range(n):
            ip = self.indx[i]
            s = x[ip]
            x[ip] = x[i]
            if ii != 0:
                for j in range(ii - 1, i):
                    s -= self.lu[i][j] * x[j]
            elif s != 0.0:
                ii = i + 1
            x[i] = s
        for i in range(n - 1, -1, -1):
            s = x[i]
            for j in range(i + 1, n):
                s -= self.lu[i][j] * x[j]
            x[i] = s / self.lu[i][i]


def intpt(a, b, c, x):
    MAXITS = 200
    EPS = 1.0e-6
    SIGMA = 0.9
    DELTA = 0.02
    BIG = 1.7976931348623157e308
    m = len(a)
    n = len(a[0])
    y = [0.0] * m
    z = [0.0] * n
    ax = [0.0] * m
    aty = [0.0] * n
    rp = [0.0] * m
    rd = [0.0] * n
    d = [0.0] * n
    dx = [0.0] * n
    dy = [0.0] * m
    dz = [0.0] * n
    rhs = [0.0] * m
    tempm = [0.0] * m
    tempn = [0.0] * n
    at = [[a[i][j] for i in range(m)] for j in range(n)]
    rpfact = 1.0 + math.sqrt(dotprod(b, b))
    rdfact = 1.0 + math.sqrt(dotprod(c, c))
    for j in range(n):
        x[j] = 1000.0
        z[j] = 1000.0
    for i in range(m):
        y[i] = 1000.0
    normrp_old = BIG
    normrd_old = BIG
    mat = [[0.0] * m for _ in range(m)]
    for _ in range(MAXITS):
        for i in range(m):
            s = 0.0
            for j in range(n):
                s += a[i][j] * x[j]
            ax[i] = s
        for i in range(m):
            rp[i] = ax[i] - b[i]
        normrp = math.sqrt(dotprod(rp, rp)) / rpfact
        for j in range(n):
            s = 0.0
            for i in range(m):
                s += at[j][i] * y[i]
            aty[j] = s
        for j in range(n):
            rd[j] = aty[j] + z[j] - c[j]
        normrd = math.sqrt(dotprod(rd, rd)) / rdfact
        gamma = dotprod(x, z)
        mu = DELTA * gamma / n
        primal_obj = dotprod(c, x)
        gamma_norm = gamma / (1.0 + abs(primal_obj))
        if normrp < EPS and normrd < EPS and gamma_norm < EPS:
            return 0
        if normrp > 1000 * normrp_old and normrp > EPS:
            return 1
        if normrd > 1000 * normrd_old and normrd > EPS:
            return 2
        for j in range(n):
            d[j] = x[j] / z[j]
        for i in range(m):
            for k in range(m):
                s = 0.0
                for j in range(n):
                    s += a[i][j] * d[j] * a[k][j]
                mat[i][k] = s
        for j in range(n):
            tempn[j] = x[j] - mu / z[j] - d[j] * rd[j]
        for i in range(m):
            s = 0.0
            for j in range(n):
                s += a[i][j] * tempn[j]
            tempm[i] = s
        for i in range(m):
            rhs[i] = -rp[i] + tempm[i]
        try:
            alu = LUdcmp(mat)
            alu.solve(rhs, dy)
        except Singular:
            return 3
        for j in range(n):
            s = 0.0
            for i in range(m):
                s += at[j][i] * dy[i]
            tempn[j] = s
        for j in range(n):
            dz[j] = -tempn[j] - rd[j]
        for j in range(n):
            dx[j] = -d[j] * dz[j] + mu / z[j] - x[j]
        alpha_p = 1.0
        for j in range(n):
            if x[j] + alpha_p * dx[j] < 0.0:
                alpha_p = -x[j] / dx[j]
        alpha_d = 1.0
        for j in range(n):
            if z[j] + alpha_d * dz[j] < 0.0:
                alpha_d = -z[j] / dz[j]
        alpha_p = min(alpha_p * SIGMA, 1.0)
        alpha_d = min(alpha_d * SIGMA, 1.0)
        for j in range(n):
            x[j] += alpha_p * dx[j]
            z[j] += alpha_d * dz[j]
        for i in range(m):
            y[i] += alpha_d * dy[i]
        normrp_old = normrp
        normrd_old = normrd
    return 3


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
    p = 1
    m = int(toks[p])
    n = int(toks[p + 1])
    p += 2
    a = []
    for _ in range(m):
        a.append([float(toks[p + j]) for j in range(n)])
        p += n
    b = [float(toks[p + i]) for i in range(m)]
    p += m
    c = [float(toks[p + j]) for j in range(n)]
    p += n
    if op == "INTPT":
        x = [0.0] * n
        status = intpt(a, b, c, x)
        print(" ".join(fmt6(v) for v in x) + " %d" % status)


main()
