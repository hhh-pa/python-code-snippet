# Incomplete gamma and error functions (NR 6.2).
import math
import sys

GCOF = [57.1562356658629235, -59.5979603554754912, 14.1360979747417471,
        -0.491913816097620199, 0.339946499848118887e-4, 0.465236289270485756e-4,
        -0.983744753048795646e-4, 0.158088703224912494e-3, -0.210264441724104883e-3,
        0.217439618115212643e-3, -0.164318106536763890e-3, 0.844182239838527433e-4,
        -0.261908384015814087e-4, 0.368991826595316234e-5]

ERFCOF = [-1.3026537197817094, 6.4196979235649026e-1, 1.9476473204185836e-2,
          -9.561514786808631e-3, -9.46595344482036e-4, 3.66839497852761e-4,
          4.2523324806907e-5, -2.0278578112534e-5, -1.624290004647e-6,
          1.303655835580e-6, 1.5626441722e-8, -8.5238095915e-8,
          6.529054439e-9, 5.059343495e-9, -9.91364156e-10,
          -2.27365122e-10, 9.6467911e-11, 2.394038e-12,
          -6.886027e-12, 8.94487e-13, 3.13092e-13,
          -1.12708e-13, 3.81e-16, 7.106e-15,
          -1.523e-15, -9.4e-17, 1.21e-16, -2.8e-17]


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


def erfccheb(z):
    t = 2.0 / (2.0 + z)
    ty = 4.0 * t - 2.0
    d = 0.0
    dd = 0.0
    for j in range(27, 0, -1):
        tmp = d
        d = ty * d - dd + ERFCOF[j]
        dd = tmp
    return t * math.exp(-z * z + 0.5 * (ERFCOF[0] + ty * d) - dd)


def erfcx(x):
    return erfccheb(x) if x >= 0.0 else 2.0 - erfccheb(-x)


def inverfc(p):
    if p >= 2.0:
        return -100.0
    if p <= 0.0:
        return 100.0
    pp = p if p < 1.0 else 2.0 - p
    t = math.sqrt(-2.0 * math.log(pp / 2.0))
    x = -0.70711 * ((2.30753 + t * 0.27061) / (1.0 + t * (0.99229 + t * 0.04481)) - t)
    for _ in range(2):
        err = erfcx(x) - pp
        x += err / (1.12837916709551257 * math.exp(-x * x) - x * err)
    return x if p < 1.0 else -x


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    eps = 2.220446049250313e-16
    fpmin = 1.0020841800044864e-292
    ans = 0.0
    if op in ("GAMMP", "GAMMQ"):
        a = float(toks[1])
        x = float(toks[2])
        gln = gammln(a)
        if x == 0.0:
            ans = 0.0 if op == "GAMMP" else 1.0
        elif x < a + 1.0:
            ap = a
            dl = 1.0 / a
            sm = dl
            for _ in range(1000):
                ap += 1.0
                dl *= x / ap
                sm += dl
                if abs(dl) < abs(sm) * eps:
                    break
            p = sm * math.exp(-x + a * math.log(x) - gln)
            ans = p if op == "GAMMP" else 1.0 - p
        else:
            b = x + 1.0 - a
            c = 1.0 / fpmin
            d = 1.0 / b
            h = d
            for i in range(1, 1001):
                an = -i * (i - a)
                b += 2.0
                d = an * d + b
                if abs(d) < fpmin:
                    d = fpmin
                c = b + an / c
                if abs(c) < fpmin:
                    c = fpmin
                d = 1.0 / d
                dl = d * c
                h *= dl
                if abs(dl - 1.0) <= eps:
                    break
            q = math.exp(-x + a * math.log(x) - gln) * h
            ans = 1.0 - q if op == "GAMMP" else q
    elif op == "ERF":
        x = float(toks[1])
        ans = 1.0 - erfccheb(x) if x >= 0.0 else erfccheb(-x) - 1.0
    elif op == "ERFC":
        ans = erfcx(float(toks[1]))
    elif op == "INVERFC":
        ans = inverfc(float(toks[1]))
    else:
        ans = inverfc(1.0 - float(toks[1]))
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
