# Incomplete beta function (NR 6.4).
import math
import sys

EPS = 2.220446049250313e-16
FPMIN = 1.0020841800044864e-292

GCOF = [57.1562356658629235, -59.5979603554754912, 14.1360979747417471,
        -0.491913816097620199, 0.339946499848118887e-4, 0.465236289270485756e-4,
        -0.983744753048795646e-4, 0.158088703224912494e-3, -0.210264441724104883e-3,
        0.217439618115212643e-3, -0.164318106536763890e-3, 0.844182239838527433e-4,
        -0.261908384015814087e-4, 0.368991826595316234e-5]


def gammln(xx):
    y = xx
    x = xx
    tmp = x + 5.2421875000000000
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 0.999999999999997092
    for j in range(14):
        y += 1.0
        ser += GCOF[j] / y
    return tmp + math.log(2.5066282746310005 * ser / x)


def betacf(a, b, x):
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        dl = d * c
        h *= dl
        if abs(dl - 1.0) <= EPS:
            break
    return h


def betai(a, b, x):
    if x == 0.0 or x == 1.0:
        return x
    bt = math.exp(gammln(a + b) - gammln(a) - gammln(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def invbetai(p, a, b):
    epsi = 1.0e-8
    if p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    a1 = a - 1.0
    b1 = b - 1.0
    if a >= 1.0 and b >= 1.0:
        pp = p if p < 0.5 else 1.0 - p
        t = math.sqrt(-2.0 * math.log(pp))
        x = (2.30753 + t * 0.27061) / (1.0 + t * (0.99229 + t * 0.04481)) - t
        if p < 0.5:
            x = -x
        al = (x * x - 3.0) / 6.0
        h = 2.0 / (1.0 / (2.0 * a - 1.0) + 1.0 / (2.0 * b - 1.0))
        w = (x * math.sqrt(al + h) / h) - (1.0 / (2.0 * b - 1.0) - 1.0 / (2.0 * a - 1.0)) * \
            (al + 5.0 / 6.0 - 2.0 / (3.0 * h))
        x = a / (a + b * math.exp(2.0 * w))
    else:
        lna = math.log(a / (a + b))
        lnb = math.log(b / (a + b))
        t = math.exp(a * lna) / a
        u = math.exp(b * lnb) / b
        w = t + u
        if p < t / w:
            x = math.pow(a * w * p, 1.0 / a)
        else:
            x = 1.0 - math.pow(b * w * (1.0 - p), 1.0 / b)
    afac = -gammln(a) - gammln(b) + gammln(a + b)
    for j in range(10):
        if x == 0.0 or x == 1.0:
            return x
        err = betai(a, b, x) - p
        t = math.exp(a1 * math.log(x) + b1 * math.log(1.0 - x) + afac)
        u = err / t
        uu = u * (a1 / x - b1 / (1.0 - x))
        if uu > 1.0:
            uu = 1.0
        tt = u / (1.0 - 0.5 * uu)
        x -= tt
        if x <= 0.0:
            x = 0.5 * (x + tt)
        if x >= 1.0:
            x = 0.5 * (x + tt + 1.0)
        if abs(tt) < epsi * x and j > 0:
            break
    return x


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "BETAI":
        ans = betai(float(toks[1]), float(toks[2]), float(toks[3]))
    else:
        ans = invbetai(float(toks[1]), float(toks[2]), float(toks[3]))
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
