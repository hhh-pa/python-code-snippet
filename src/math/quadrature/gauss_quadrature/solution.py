# Gaussian quadrature rules (NR 4.6).
import math
import sys

GAMM_C = [76.18009172947146, -86.50532032941677, 24.01409824083091,
          -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]


def gammln(xx):
    y = xx
    tmp = xx + 5.5
    ser = 1.000000000190015
    tmp -= (xx + 0.5) * math.log(tmp)
    for j in range(6):
        y += 1.0
        ser += GAMM_C[j] / y
    return -tmp + math.log(2.5066282746310005 * ser / xx)


def fmtxw(x, w):
    a = 0.0 if abs(x) < 5e-7 else x
    b = 0.0 if abs(w) < 5e-7 else w
    return "%.6f %.6f" % (a + 0.0, b + 0.0)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    eps = 1.0e-14
    out = []
    if op == "LEGENDRE":
        x1 = float(toks[1])
        x2 = float(toks[2])
        n = int(toks[3])
        x = [0.0] * n
        w = [0.0] * n
        m = (n + 1) // 2
        xm = 0.5 * (x2 + x1)
        xl = 0.5 * (x2 - x1)
        for i in range(m):
            z = math.cos(3.141592654 * (i + 0.75) / (n + 0.5))
            pp = 0.0
            while True:
                p1 = 1.0
                p2 = 0.0
                for j in range(n):
                    p3 = p2
                    p2 = p1
                    p1 = ((2.0 * j + 1.0) * z * p2 - j * p3) / (j + 1)
                pp = n * (z * p1 - p2) / (z * z - 1.0)
                z1 = z
                z = z1 - p1 / pp
                if abs(z - z1) <= eps:
                    break
            x[i] = xm - xl * z
            x[n - 1 - i] = xm + xl * z
            w[i] = 2.0 * xl / ((1.0 - z * z) * pp * pp)
            w[n - 1 - i] = w[i]
        out = [fmtxw(x[i], w[i]) for i in range(n)]
    elif op == "LAGUERRE":
        alf = float(toks[1])
        n = int(toks[2])
        maxit = 10
        x = [0.0] * n
        w = [0.0] * n
        z = 0.0
        for i in range(n):
            if i == 0:
                z = (1.0 + alf) * (3.0 + 0.92 * alf) / (1.0 + 2.4 * n + 1.8 * alf)
            elif i == 1:
                z += (15.0 + 6.25 * alf) / (1.0 + 0.9 * alf + 2.5 * n)
            else:
                ai = i - 1
                z += ((1.0 + 2.55 * ai) / (1.9 * ai) + 1.26 * ai * alf / (1.0 + 3.5 * ai)) * \
                    (z - x[i - 2]) / (1.0 + 0.3 * alf)
            pp = 0.0
            p2 = 0.0
            for _ in range(maxit):
                p1 = 1.0
                p2 = 0.0
                for j in range(n):
                    p3 = p2
                    p2 = p1
                    p1 = ((2 * j + 1 + alf - z) * p2 - (j + alf) * p3) / (j + 1)
                pp = (n * p1 - (n + alf) * p2) / z
                z1 = z
                z = z1 - p1 / pp
                if abs(z - z1) <= eps:
                    break
            x[i] = z
            w[i] = -math.exp(gammln(alf + n) - gammln(n)) / (pp * n * p2)
        out = [fmtxw(x[i], w[i]) for i in range(n)]
    elif op == "HERMITE":
        n = int(toks[1])
        pim4 = 0.7511255444649425
        maxit = 10
        x = [0.0] * n
        w = [0.0] * n
        m = (n + 1) // 2
        z = 0.0
        for i in range(m):
            if i == 0:
                z = math.sqrt(2 * n + 1) - 1.85575 * math.pow(2 * n + 1, -0.16667)
            elif i == 1:
                z -= 1.14 * math.pow(n, 0.426) / z
            elif i == 2:
                z = 1.86 * z - 0.86 * x[0]
            elif i == 3:
                z = 1.91 * z - 0.91 * x[1]
            else:
                z = 2.0 * z - x[i - 2]
            pp = 0.0
            for _ in range(maxit):
                p1 = pim4
                p2 = 0.0
                for j in range(n):
                    p3 = p2
                    p2 = p1
                    p1 = z * math.sqrt(2.0 / (j + 1)) * p2 - math.sqrt(j / (j + 1)) * p3
                pp = math.sqrt(2 * n) * p2
                z1 = z
                z = z1 - p1 / pp
                if abs(z - z1) <= eps:
                    break
            x[i] = z
            x[n - 1 - i] = -z
            w[i] = 2.0 / (pp * pp)
            w[n - 1 - i] = w[i]
        out = [fmtxw(x[i], w[i]) for i in range(n)]
    else:
        alf = float(toks[1])
        bet = float(toks[2])
        n = int(toks[3])
        maxit = 10
        x = [0.0] * n
        w = [0.0] * n
        z = 0.0
        for i in range(n):
            if i == 0:
                an = alf / n
                bn = bet / n
                r1 = (1.0 + alf) * (2.78 / (4.0 + n * n) + 0.768 * an / n)
                r2 = 1.0 + 1.48 * an + 0.96 * bn + 0.452 * an * an + 0.83 * an * bn
                z = 1.0 - r1 / r2
            elif i == 1:
                r1 = (4.1 + alf) / ((1.0 + alf) * (1.0 + 0.156 * alf))
                r2 = 1.0 + 0.06 * (n - 8.0) * (1.0 + 0.12 * alf) / n
                r3 = 1.0 + 0.012 * bet * (1.0 + 0.25 * abs(alf)) / n
                z -= (1.0 - z) * r1 * r2 * r3
            elif i == 2:
                r1 = (1.67 + 0.28 * alf) / (1.0 + 0.37 * alf)
                r2 = 1.0 + 0.22 * (n - 8.0) / n
                r3 = 1.0 + 8.0 * bet / ((6.28 + bet) * n * n)
                z -= (x[0] - z) * r1 * r2 * r3
            elif i == n - 2:
                r1 = (1.0 + 0.235 * bet) / (0.766 + 0.119 * bet)
                r2 = 1.0 / (1.0 + 0.639 * (n - 4.0) / (1.0 + 0.71 * (n - 4.0)))
                r3 = 1.0 / (1.0 + 20.0 * alf / ((7.5 + alf) * n * n))
                z += (z - x[n - 4]) * r1 * r2 * r3
            elif i == n - 1:
                r1 = (1.0 + 0.37 * bet) / (1.67 + 0.28 * bet)
                r2 = 1.0 / (1.0 + 0.22 * (n - 8.0) / n)
                r3 = 1.0 / (1.0 + 8.0 * alf / ((6.28 + alf) * n * n))
                z += (z - x[n - 3]) * r1 * r2 * r3
            else:
                z = 3.0 * x[i - 1] - 3.0 * x[i - 2] + x[i - 3]
            alfbet = alf + bet
            temp = 2.0 + alfbet
            pp = 0.0
            p2 = 1.0
            for _ in range(1, maxit + 1):
                temp = 2.0 + alfbet
                p1 = (alf - bet + temp * z) / 2.0
                p2 = 1.0
                for j in range(2, n + 1):
                    p3 = p2
                    p2 = p1
                    temp = 2 * j + alfbet
                    a = 2 * j * (j + alfbet) * (temp - 2.0)
                    b = (temp - 1.0) * (alf * alf - bet * bet + temp * (temp - 2.0) * z)
                    c = 2.0 * (j - 1 + alf) * (j - 1 + bet) * temp
                    p1 = (b * p2 - c * p3) / a
                pp = (n * (alf - bet - temp * z) * p1 + 2.0 * (n + alf) * (n + bet) * p2) / \
                    (temp * (1.0 - z * z))
                z1 = z
                z = z1 - p1 / pp
                if abs(z - z1) <= eps:
                    break
            x[i] = z
            w[i] = math.exp(gammln(alf + n) + gammln(bet + n) - gammln(n + 1.0) -
                            gammln(n + alfbet + 1.0)) * temp * math.pow(2.0, alfbet) / (pp * p2)
        out = [fmtxw(x[i], w[i]) for i in range(n)]
    sys.stdout.write("\n".join(out) + "\n")


main()
