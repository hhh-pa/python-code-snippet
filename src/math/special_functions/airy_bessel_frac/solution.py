# Fractional Bessel, Airy, spherical Bessel (NR 6.6).
import math
import sys


def gammln(xx):
    cof = [57.1562356658629235, -59.5979603554754912, 14.1360979747417471,
           -0.491913816097620199, 0.339946499848118887e-4, 0.465236289270485756e-4,
           -0.983744753048795646e-4, 0.158088703224912494e-3, -0.210264441724104883e-3,
           0.217439618115212643e-3, -0.164318106536763890e-3, 0.844182239838527433e-4,
           -0.261908384015814087e-4, 0.368991826595316234e-5]
    y = xx
    x = xx
    tmp = x + 5.2421875000000000
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 0.999999999999997092
    for j in range(14):
        y += 1.0
        ser += cof[j] / y
    return tmp + math.log(2.5066282746310005 * ser / x)


def gammafn(x):
    prod = 1.0
    t = x
    while t <= 0.0:
        prod *= t
        t += 1.0
    return math.exp(gammln(t)) / prod


def jfrac(nu, x):
    h = x / 2.0
    t = math.pow(h, nu) / gammafn(nu + 1.0)
    s = t
    q = h * h
    for k in range(1, 81):
        t *= -q / (k * (k + nu))
        s += t
    return s


def yfrac(nu, x):
    return (jfrac(nu, x) * math.cos(nu * math.pi) - jfrac(-nu, x)) / math.sin(nu * math.pi)


def ifrac(nu, x):
    h = x / 2.0
    t = math.pow(h, nu) / gammafn(nu + 1.0)
    s = t
    q = h * h
    for k in range(1, 81):
        t *= q / (k * (k + nu))
        s += t
    return s


def aserf(x, nu, nterms, alt):
    mu = 4.0 * nu * nu
    r = 1.0 / (8.0 * x)
    c = 1.0
    pw = 1.0
    s = 1.0
    for k in range(1, nterms + 1):
        c *= (mu - (2 * k - 1.0) * (2 * k - 1.0)) / k
        pw *= r
        s += (-1.0 if alt and k % 2 == 1 else 1.0) * c * pw
    return s


def kfrac(nu, x):
    if x < 6.0:
        return math.pi * (ifrac(-nu, x) - ifrac(nu, x)) / (2.0 * math.sin(nu * math.pi))
    return math.sqrt(math.pi / (2.0 * x)) * math.exp(-x) * aserf(x, nu, 16, False)


def airy(x):
    onovrt = 0.577350269189626
    if x == 0.0:
        g23 = gammafn(2.0 / 3.0)
        g13 = gammafn(1.0 / 3.0)
        return (1.0 / (math.pow(3.0, 2.0 / 3.0) * g23),
                1.0 / (math.pow(3.0, 1.0 / 6.0) * g23),
                -1.0 / (math.pow(3.0, 1.0 / 3.0) * g13),
                math.pow(3.0, 1.0 / 6.0) / g13)
    ax = abs(x)
    rootx = math.sqrt(ax)
    z = (2.0 / 3.0) * ax * rootx
    if x > 0.0:
        io = ifrac(1.0 / 3.0, z)
        ko = kfrac(1.0 / 3.0, z)
        ai = rootx * onovrt * ko / math.pi
        bi = rootx * (ko / math.pi + 2.0 * onovrt * io)
        io2 = ifrac(2.0 / 3.0, z)
        ko2 = kfrac(2.0 / 3.0, z)
        aip = -x * onovrt * ko2 / math.pi
        bip = x * (ko2 / math.pi + 2.0 * onovrt * io2)
        return ai, bi, aip, bip
    jo = jfrac(1.0 / 3.0, z)
    yo = yfrac(1.0 / 3.0, z)
    ai = 0.5 * rootx * (jo - onovrt * yo)
    bi = -0.5 * rootx * (yo + onovrt * jo)
    jo2 = jfrac(2.0 / 3.0, z)
    yo2 = yfrac(2.0 / 3.0, z)
    aip = 0.5 * ax * (jo2 + onovrt * yo2)
    bip = 0.5 * ax * (onovrt * jo2 - yo2)
    return ai, bi, aip, bip


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op in ("JFRAC", "YFRAC", "IFRAC", "KFRAC"):
        nu = float(toks[1])
        x = float(toks[2])
        if op == "JFRAC":
            ans = jfrac(nu, x)
        elif op == "YFRAC":
            ans = yfrac(nu, x)
        elif op == "IFRAC":
            ans = ifrac(nu, x)
        else:
            ans = kfrac(nu, x)
    elif op in ("AI", "BI", "AIP", "BIP"):
        ai, bi, aip, bip = airy(float(toks[1]))
        if op == "AI":
            ans = ai
        elif op == "BI":
            ans = bi
        elif op == "AIP":
            ans = aip
        else:
            ans = bip
    else:
        n = int(toks[1])
        x = float(toks[2])
        rtpio2 = 1.253314137315500251
        nu = n + 0.5
        factor = rtpio2 / math.sqrt(x)
        jo = jfrac(nu, x)
        yo = yfrac(nu, x)
        jo1 = jfrac(nu + 1.0, x)
        yo1 = yfrac(nu + 1.0, x)
        jpo = (nu / x) * jo - jo1
        ypo = (nu / x) * yo - yo1
        sj = factor * jo
        sy = factor * yo
        if op == "SPHJ":
            ans = sj
        elif op == "SPHY":
            ans = sy
        elif op == "SPHJP":
            ans = factor * jpo - sj / (2.0 * x)
        else:
            ans = factor * ypo - sy / (2.0 * x)
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
