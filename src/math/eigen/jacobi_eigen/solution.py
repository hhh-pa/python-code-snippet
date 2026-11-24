# All eigenvalues and eigenvectors of a real symmetric
# matrix by Jacobi's cyclic method (with eigsrt).
# Reference: Press et al., Numerical Recipes 3e, Section 11.1.
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


def rot(a, s, tau, i, j, k, l):
    g = a[i][j]
    h = a[k][l]
    a[i][j] = g - s * (h + g * tau)
    a[k][l] = h + s * (g - h * tau)


class TooMany(Exception):
    pass


class Jacobi:
    def __init__(self, aa):
        EPS = 2.220446049250313e-16
        n = len(aa)
        self.n = n
        a = [list(row) for row in aa]
        v = [[0.0] * n for _ in range(n)]
        d = [0.0] * n
        self.nrot = 0
        b = [0.0] * n
        z = [0.0] * n
        for ip in range(n):
            for iq in range(n):
                v[ip][iq] = 0.0
            v[ip][ip] = 1.0
        for ip in range(n):
            b[ip] = d[ip] = a[ip][ip]
            z[ip] = 0.0
        for i in range(1, 51):
            sm = 0.0
            for ip in range(n - 1):
                for iq in range(ip + 1, n):
                    sm += abs(a[ip][iq])
            if sm == 0.0:
                eigsrt(d, v)
                self.d = d
                self.v = v
                return
            if i < 4:
                tresh = 0.2 * sm / (n * n)
            else:
                tresh = 0.0
            for ip in range(n - 1):
                for iq in range(ip + 1, n):
                    g = 100.0 * abs(a[ip][iq])
                    if i > 4 and g <= EPS * abs(d[ip]) and g <= EPS * abs(d[iq]):
                        a[ip][iq] = 0.0
                    elif abs(a[ip][iq]) > tresh:
                        h = d[iq] - d[ip]
                        if g <= EPS * abs(h):
                            t = a[ip][iq] / h
                        else:
                            theta = 0.5 * h / a[ip][iq]
                            t = 1.0 / (abs(theta) + math.sqrt(1.0 + theta * theta))
                            if theta < 0.0:
                                t = -t
                        c = 1.0 / math.sqrt(1 + t * t)
                        s = t * c
                        tau = s / (1.0 + c)
                        h = t * a[ip][iq]
                        z[ip] -= h
                        z[iq] += h
                        d[ip] -= h
                        d[iq] += h
                        a[ip][iq] = 0.0
                        for j in range(ip):
                            rot(a, s, tau, j, ip, j, iq)
                        for j in range(ip + 1, iq):
                            rot(a, s, tau, ip, j, j, iq)
                        for j in range(iq + 1, n):
                            rot(a, s, tau, ip, j, iq, j)
                        for j in range(n):
                            rot(v, s, tau, j, ip, j, iq)
                        self.nrot += 1
            for ip in range(n):
                b[ip] += z[ip]
                d[ip] = b[ip]
                z[ip] = 0.0
        raise TooMany()


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
    vals = [float(t) for t in toks[2:2 + n * n]]
    a = [vals[i * n:(i + 1) * n] for i in range(n)]
    if op == "JACOBI":
        try:
            jb = Jacobi(a)
            parts = [fmt6(v) for v in jb.d]
            for i in range(n):
                for j in range(n):
                    parts.append(fmt6(jb.v[i][j]))
            parts.append(str(jb.nrot))
            parts.append("0")
            print(" ".join(parts))
        except TooMany:
            print(" ".join(["0.000000"] * (n + n * n)) + " 0 1")


main()
