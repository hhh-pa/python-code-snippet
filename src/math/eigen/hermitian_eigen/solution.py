# All eigenvalues and eigenvectors of a Hermitian matrix
# via reduction to a real symmetric 2n x 2n problem
# (solved by Householder+QL), choosing one from each
# doubled eigenpair.
# Reference: Press et al., Numerical Recipes 3e, Section 11.5.
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys


def eigsrt(d, v):
    n = len(d)
    for i in range(n - 1):
        k = i
        p = d[k]
        for j in range(i, n):
            if d[j] >= p:
                k = j
                p = d[k]
        if k != i:
            d[k] = d[i]
            d[i] = p
            for j in range(n):
                p = v[j][i]
                v[j][i] = v[j][k]
                v[j][k] = p


class TooMany(Exception):
    pass


class Symmeig:
    def __init__(self, a):
        n = len(a)
        self.n = n
        self.z = [list(row) for row in a]
        self.d = [0.0] * n
        self.e = [0.0] * n
        self.tred2()
        self.tqli()
        eigsrt(self.d, self.z)

    def tred2(self):
        n = self.n
        z = self.z
        d = self.d
        e = self.e
        for i in range(n - 1, 0, -1):
            l = i - 1
            h = 0.0
            scale = 0.0
            if l > 0:
                for k in range(i):
                    scale += abs(z[i][k])
                if scale == 0.0:
                    e[i] = z[i][l]
                else:
                    for k in range(i):
                        z[i][k] /= scale
                        h += z[i][k] * z[i][k]
                    f = z[i][l]
                    g = -math.sqrt(h) if f >= 0.0 else math.sqrt(h)
                    e[i] = scale * g
                    h -= f * g
                    z[i][l] = f - g
                    f = 0.0
                    for j in range(i):
                        z[j][i] = z[i][j] / h
                        g = 0.0
                        for k in range(j + 1):
                            g += z[j][k] * z[i][k]
                        for k in range(j + 1, i):
                            g += z[k][j] * z[i][k]
                        e[j] = g / h
                        f += e[j] * z[i][j]
                    hh = f / (h + h)
                    for j in range(i):
                        f = z[i][j]
                        e[j] = g = e[j] - hh * f
                        for k in range(j + 1):
                            z[j][k] -= (f * e[k] + g * z[i][k])
            else:
                e[i] = z[i][l]
            d[i] = h
        d[0] = 0.0
        e[0] = 0.0
        for i in range(n):
            if d[i] != 0.0:
                for j in range(i):
                    g = 0.0
                    for k in range(i):
                        g += z[i][k] * z[k][j]
                    for k in range(i):
                        z[k][j] -= g * z[k][i]
            d[i] = z[i][i]
            z[i][i] = 1.0
            for j in range(i):
                z[j][i] = z[i][j] = 0.0

    def tqli(self):
        EPS = 2.220446049250313e-16
        n = self.n
        d = self.d
        e = self.e
        z = self.z
        for i in range(1, n):
            e[i - 1] = e[i]
        e[n - 1] = 0.0
        for l in range(n):
            it = 0
            while True:
                m = l
                while m < n - 1:
                    dd = abs(d[m]) + abs(d[m + 1])
                    if abs(e[m]) <= EPS * dd:
                        break
                    m += 1
                if m == l:
                    break
                if it == 30:
                    raise TooMany()
                it += 1
                g = (d[l + 1] - d[l]) / (2.0 * e[l])
                r = self.pythag(g, 1.0)
                g = d[m] - d[l] + e[l] / (g + (r if g >= 0.0 else -r))
                s = 1.0
                c = 1.0
                p = 0.0
                i = m - 1
                while i >= l:
                    f = s * e[i]
                    b = c * e[i]
                    r = self.pythag(f, g)
                    e[i + 1] = r
                    if r == 0.0:
                        d[i + 1] -= p
                        e[m] = 0.0
                        break
                    s = f / r
                    c = g / r
                    g = d[i + 1] - p
                    r = (d[i] - g) * s + 2.0 * c * b
                    p = s * r
                    d[i + 1] = g + p
                    g = c * r - b
                    for k in range(n):
                        f = z[k][i + 1]
                        z[k][i + 1] = s * z[k][i] + c * f
                        z[k][i] = c * z[k][i] - s * f
                    i -= 1
                if r == 0.0 and i >= l:
                    continue
                d[l] -= p
                e[l] = g
                e[m] = 0.0

    def pythag(self, a, b):
        absa = abs(a)
        absb = abs(b)
        if absa > absb:
            return absa * math.sqrt(1.0 + (absb / absa) * (absb / absa))
        elif absb == 0.0:
            return 0.0
        else:
            return absb * math.sqrt(1.0 + (absa / absb) * (absa / absb))


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
    n = int(toks[1])
    vals = [float(t) for t in toks[2:]]
    amat = [vals[i * n:(i + 1) * n] for i in range(n)]
    bmat = [vals[n * n + i * n:n * n + (i + 1) * n] for i in range(n)]
    if op == "HERMITIAN":
        try:
            m = 2 * n
            aug = [[0.0] * m for _ in range(m)]
            for i in range(n):
                for j in range(n):
                    aug[i][j] = amat[i][j]
                    aug[i][j + n] = -bmat[i][j]
                    aug[i + n][j] = bmat[i][j]
                    aug[i + n][j + n] = amat[i][j]
            se = Symmeig(aug)
            parts = [fmt6(se.d[2 * k]) for k in range(n)]
            for k in range(n):
                for j in range(n):
                    parts.append(fmt6(se.z[j][2 * k]))
            for k in range(n):
                for j in range(n):
                    parts.append(fmt6(se.z[j + n][2 * k]))
            parts.append("0")
            print(" ".join(parts))
        except TooMany:
            print(" ".join(["0.000000"] * (n + 2 * n * n)) + " 1")


main()
