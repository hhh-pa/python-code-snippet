# Statistical distributions (NR 6.14).
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

GEPS = 2.220446049250313e-16
GFPMIN = 1.0020841800044864e-292


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


def gammp(a, x):
    gln = gammln(a)
    if x == 0.0:
        return 0.0
    if x < a + 1.0:
        ap = a
        dl = 1.0 / a
        sm = dl
        for _ in range(1000):
            ap += 1.0
            dl *= x / ap
            sm += dl
            if abs(dl) < abs(sm) * GEPS:
                break
        return sm * math.exp(-x + a * math.log(x) - gln)
    b = x + 1.0 - a
    c = 1.0 / GFPMIN
    d = 1.0 / b
    h = d
    for i in range(1, 1001):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < GFPMIN:
            d = GFPMIN
        c = b + an / c
        if abs(c) < GFPMIN:
            c = GFPMIN
        d = 1.0 / d
        dl = d * c
        h *= dl
        if abs(dl - 1.0) <= GEPS:
            break
    return 1.0 - math.exp(-x + a * math.log(x) - gln) * h


def gammq(a, x):
    gln = gammln(a)
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        ap = a
        dl = 1.0 / a
        sm = dl
        for _ in range(1000):
            ap += 1.0
            dl *= x / ap
            sm += dl
            if abs(dl) < abs(sm) * GEPS:
                break
        return 1.0 - sm * math.exp(-x + a * math.log(x) - gln)
    b = x + 1.0 - a
    c = 1.0 / GFPMIN
    d = 1.0 / b
    h = d
    for i in range(1, 1001):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < GFPMIN:
            d = GFPMIN
        c = b + an / c
        if abs(c) < GFPMIN:
            c = GFPMIN
        d = 1.0 / d
        dl = d * c
        h *= dl
        if abs(dl - 1.0) <= GEPS:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


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


def betacf(a, b, x):
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < GFPMIN:
        d = GFPMIN
    d = 1.0 / d
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < GFPMIN:
            d = GFPMIN
        c = 1.0 + aa / c
        if abs(c) < GFPMIN:
            c = GFPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < GFPMIN:
            d = GFPMIN
        c = 1.0 + aa / c
        if abs(c) < GFPMIN:
            c = GFPMIN
        d = 1.0 / d
        dl = d * c
        h *= dl
        if abs(dl - 1.0) <= GEPS:
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


def invgammp(p, a):
    eps = 1.0e-8
    gln = gammln(a)
    a1 = a - 1.0
    if p >= 1.0:
        return max(100.0, a + 100.0 * math.sqrt(a))
    if p <= 0.0:
        return 0.0
    if a > 1.0:
        lna1 = math.log(a1)
        afac = math.exp(a1 * (lna1 - 1.0) - gln)
        pp = p if p < 0.5 else 1.0 - p
        t = math.sqrt(-2.0 * math.log(pp))
        x = (2.30753 + t * 0.27061) / (1.0 + t * (0.99229 + t * 0.04481)) - t
        if p < 0.5:
            x = -x
        x = max(1.0e-3, a * math.pow(1.0 - 1.0 / (9.0 * a) - x / (3.0 * math.sqrt(a)), 3))
    else:
        t = 1.0 - a * (0.253 + a * 0.12)
        if p < t:
            x = math.pow(p / t, 1.0 / a)
        else:
            x = 1.0 - math.log(1.0 - (p - t) / (1.0 - t))
    for _ in range(12):
        if x <= 0.0:
            return 0.0
        err = gammp(a, x) - p
        if a > 1.0:
            t = afac * math.exp(-(x - a1) + a1 * (math.log(x) - lna1))
        else:
            t = math.exp(-x + a1 * math.log(x) - gln)
        u = err / t
        uu = u * ((a - 1.0) / x - 1.0)
        if uu > 1.0:
            uu = 1.0
        tt = u / (1.0 - 0.5 * uu)
        x -= tt
        t = tt
        if x <= 0.0:
            x = 0.5 * (x + t)
        if abs(t) < eps * x:
            break
    return x


def invxlogx(y):
    ooe = 0.367879441171442322
    to = 0.0
    if y < -0.2:
        u = math.log(ooe - math.sqrt(2.0 * ooe * (y + ooe)))
    else:
        u = -10.0
    while True:
        t = (math.log(y / u) - u) * (u / (1.0 + u))
        u += t
        if t < 1.0e-8 and abs(t + to) < 0.01 * abs(t):
            break
        to = t
        if not abs(t / u) > 1.0e-15:
            break
    return math.exp(u)


def pks(z):
    if z == 0.0:
        return 0.0
    if z < 1.18:
        y = math.exp(-1.23370055013616983 / (z * z))
        return 2.25675833419102515 * math.sqrt(-math.log(y)) * \
            (y + math.pow(y, 9) + math.pow(y, 25) + math.pow(y, 49))
    x = math.exp(-2.0 * z * z)
    return 1.0 - 2.0 * (x - math.pow(x, 4) + math.pow(x, 9))


def qks(z):
    if z == 0.0:
        return 1.0
    if z < 1.18:
        return 1.0 - pks(z)
    x = math.exp(-2.0 * z * z)
    return 2.0 * (x - math.pow(x, 4) + math.pow(x, 9))


def invqks(q):
    if q == 1.0:
        return 0.0
    if q > 0.3:
        t1 = 1.0 - q
        f = -0.392699081698724155 * t1 * t1
        y = invxlogx(f)
        while True:
            logy = math.log(y)
            s = 1.0 + math.pow(y, 4) + math.pow(y, 12)
            ff = f / (s * s)
            u = (y * logy - ff) / (1.0 + logy)
            t = u / max(0.5, 1.0 - 0.5 * u / (y * (1.0 + logy)))
            y -= t
            if not abs(t / y) > 1.0e-15:
                break
        return 1.57079632679489662 / math.sqrt(-math.log(y))
    x = 0.03
    while True:
        xp = x
        x = 0.5 * q + math.pow(x, 4) - math.pow(x, 9)
        if x > 0.06:
            x += math.pow(x, 16) - math.pow(x, 25)
        if not abs((xp - x) / x) > 1.0e-15:
            break
    return math.sqrt(-0.5 * math.log(x))


def poisson_cdf(lam, n):
    if n == 0:
        return 0.0
    return gammq(float(n), lam)


def poisson_inv(lam, p):
    if p < math.exp(-lam):
        return 0
    n = int(max(math.sqrt(lam), 5.0))
    inc = 1
    if p < poisson_cdf(lam, n):
        while True:
            n = n - inc if n - inc > 0 else 0
            inc *= 2
            if not p < poisson_cdf(lam, n):
                break
        nl = n
        nu = n + inc // 2
    else:
        while True:
            n += inc
            inc *= 2
            if not p > poisson_cdf(lam, n):
                break
        nu = n
        nl = n - inc // 2
    while nu - nl > 1:
        n = (nl + nu) // 2
        if p < poisson_cdf(lam, n):
            nu = n
        else:
            nl = n
    return nl


def binomial_cdf(n, pe, k):
    if k == 0:
        return 0.0
    if k > n:
        return 1.0
    return 1.0 - betai(float(k), float(n - k + 1), pe)


def binomial_inv(n, pe, p):
    k = int(n * pe)
    if k < 0:
        k = 0
    if k > n:
        k = n
    inc = 1
    if p < binomial_cdf(n, pe, k):
        while True:
            k = k - inc if k - inc > 0 else 0
            inc *= 2
            if not p < binomial_cdf(n, pe, k):
                break
        kl = k
        ku = k + inc // 2
    else:
        while True:
            k = k + inc if k + inc < n + 1 else n + 1
            inc *= 2
            if not p > binomial_cdf(n, pe, k):
                break
        ku = k
        kl = k - inc // 2
    while ku - kl > 1:
        k = (kl + ku) // 2
        if p < binomial_cdf(n, pe, k):
            ku = k
        else:
            kl = k
    return kl


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "NORMAL":
        mu, sig, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = 0.5 * erfcx(-0.707106781186547524 * (x - mu) / sig)
    elif op == "NORMAL_INV":
        mu, sig, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = -1.41421356237309505 * sig * inverfc(2.0 * p) + mu
    elif op == "CAUCHY":
        mu, sig, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = 0.5 + 0.318309886183790671 * math.atan2(x - mu, sig)
    elif op == "CAUCHY_INV":
        mu, sig, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = mu + sig * math.tan(3.14159265358979324 * (p - 0.5))
    elif op == "STUDENTT":
        nu, mu, sig, t = float(toks[1]), float(toks[2]), float(toks[3]), float(toks[4])
        z = (t - mu) / sig
        p = 0.5 * betai(0.5 * nu, 0.5, nu / (nu + z * z))
        ans = 1.0 - p if t >= mu else p
    elif op == "STUDENTT_INV":
        nu, mu, sig, p = float(toks[1]), float(toks[2]), float(toks[3]), float(toks[4])
        x = invbetai(2.0 * min(p, 1.0 - p), 0.5 * nu, 0.5)
        x = sig * math.sqrt(nu * (1.0 - x) / x)
        ans = mu + x if p >= 0.5 else mu - x
    elif op == "STUDENTT_AA":
        nu, t = float(toks[1]), float(toks[2])
        ans = 1.0 - betai(0.5 * nu, 0.5, nu / (nu + t * t))
    elif op == "STUDENTT_INVAA":
        nu, p = float(toks[1]), float(toks[2])
        x = invbetai(1.0 - p, 0.5 * nu, 0.5)
        ans = math.sqrt(nu * (1.0 - x) / x)
    elif op == "LOGISTIC":
        mu, sig, x = float(toks[1]), float(toks[2]), float(toks[3])
        e = math.exp(-abs(1.81379936423421785 * (x - mu) / sig))
        ans = 1.0 / (1.0 + e) if x >= mu else e / (1.0 + e)
    elif op == "LOGISTIC_INV":
        mu, sig, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = mu + 0.551328895421792049 * sig * math.log(p / (1.0 - p))
    elif op == "EXPON":
        bet, x = float(toks[1]), float(toks[2])
        ans = 1.0 - math.exp(-bet * x)
    elif op == "EXPON_INV":
        bet, p = float(toks[1]), float(toks[2])
        ans = -math.log(1.0 - p) / bet
    elif op == "WEIBULL":
        alph, bet, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = 1.0 - math.exp(-math.pow(x / bet, alph))
    elif op == "WEIBULL_INV":
        alph, bet, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = bet * math.pow(-math.log(1.0 - p), 1.0 / alph)
    elif op == "LOGNORMAL":
        mu, sig, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = 0.0 if x == 0.0 else 0.5 * erfcx(-0.707106781186547524 * (math.log(x) - mu) / sig)
    elif op == "LOGNORMAL_INV":
        mu, sig, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = math.exp(-1.41421356237309505 * sig * inverfc(2.0 * p) + mu)
    elif op == "CHISQ":
        nu, x = float(toks[1]), float(toks[2])
        ans = gammp(0.5 * nu, 0.5 * x)
    elif op == "CHISQ_INV":
        nu, p = float(toks[1]), float(toks[2])
        ans = 2.0 * invgammp(p, 0.5 * nu)
    elif op == "GAMMA":
        alph, bet, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = gammp(alph, bet * x)
    elif op == "GAMMA_INV":
        alph, bet, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = invgammp(p, alph) / bet
    elif op == "FDIST":
        nu1, nu2, f = float(toks[1]), float(toks[2]), float(toks[3])
        ans = betai(0.5 * nu1, 0.5 * nu2, nu1 * f / (nu2 + nu1 * f))
    elif op == "FDIST_INV":
        nu1, nu2, p = float(toks[1]), float(toks[2]), float(toks[3])
        x = invbetai(p, 0.5 * nu1, 0.5 * nu2)
        ans = nu2 * x / (nu1 * (1.0 - x))
    elif op == "BETA":
        alph, bet, x = float(toks[1]), float(toks[2]), float(toks[3])
        ans = betai(alph, bet, x)
    elif op == "BETA_INV":
        alph, bet, p = float(toks[1]), float(toks[2]), float(toks[3])
        ans = invbetai(p, alph, bet)
    elif op == "KS_P":
        ans = pks(float(toks[1]))
    elif op == "KS_Q":
        ans = qks(float(toks[1]))
    elif op == "KS_INVQ":
        ans = invqks(float(toks[1]))
    elif op == "KS_INVP":
        ans = invqks(1.0 - float(toks[1]))
    elif op == "POISSON":
        lam, n = float(toks[1]), int(toks[2])
        ans = poisson_cdf(lam, n)
    elif op == "POISSON_INV":
        sys.stdout.write("%d\n" % poisson_inv(float(toks[1]), float(toks[2])))
        return
    elif op == "BINOMIAL":
        n, pe, k = int(toks[1]), float(toks[2]), int(toks[3])
        ans = binomial_cdf(n, pe, k)
    elif op == "BINOMIAL_INV":
        sys.stdout.write("%d\n" % binomial_inv(int(toks[1]), float(toks[2]), float(toks[3])))
        return
    else:
        return
    sys.stdout.write("%.6f\n" % (canon(ans) + 0.0))


main()
