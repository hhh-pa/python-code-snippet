# Integer Bessel functions (NR 6.5).
import math
import sys

EULER = 0.577215664901533


def j0s(x):
    q = x * x / 4.0
    term = 1.0
    s = 1.0
    for k in range(1, 41):
        term *= -q / (k * k)
        s += term
    return s


def j1s(x):
    q = x * x / 4.0
    term = 1.0
    s = 1.0
    for k in range(1, 41):
        term *= -q / (k * (k + 1.0))
        s += term
    return 0.5 * x * s


def pqjy(x, nu):
    mu = 4.0 * nu * nu
    r = 1.0 / (8.0 * x)
    c = 1.0
    pw = 1.0
    p = 1.0
    q = 0.0
    for k in range(1, 11):
        c *= (mu - (2 * k - 1.0) * (2 * k - 1.0)) / k
        pw *= r
        if k % 2 == 0:
            p += (1.0 if (k // 2) % 2 == 0 else -1.0) * c * pw
        else:
            q += (1.0 if ((k - 1) // 2) % 2 == 0 else -1.0) * c * pw
    return p, q


def j0f(x):
    ax = abs(x)
    if ax < 8.0:
        return j0s(x)
    p, q = pqjy(ax, 0)
    chi = ax - math.pi / 4.0
    return math.sqrt(2.0 / (math.pi * ax)) * (p * math.cos(chi) - q * math.sin(chi))


def j1f(x):
    ax = abs(x)
    if ax < 8.0:
        v = j1s(ax)
    else:
        p, q = pqjy(ax, 1)
        chi = ax - math.pi / 2.0 - math.pi / 4.0
        v = math.sqrt(2.0 / (math.pi * ax)) * (p * math.cos(chi) - q * math.sin(chi))
    return -v if x < 0.0 else v


def y0s(x):
    q = x * x / 4.0
    m = 1.0
    h = 0.0
    s = 0.0
    sgn = 1.0
    for k in range(1, 41):
        m *= q / (k * k)
        h += 1.0 / k
        s += sgn * h * m
        sgn = -sgn
    return (2.0 / math.pi) * ((math.log(x / 2.0) + EULER) * j0s(x) + s)


def y1s(x):
    pw = x / 2.0
    h = 0.0
    s = 0.0
    sgn = 1.0
    for k in range(41):
        hp1 = h + 1.0 / (k + 1.0)
        s += sgn * (h + hp1) * pw
        h = hp1
        sgn = -sgn
        pw *= (x * x / 4.0) / ((k + 1.0) * (k + 2.0))
    return (2.0 / math.pi) * (math.log(x / 2.0) + EULER) * j1s(x) - 2.0 / (math.pi * x) - s / math.pi


def y0f(x):
    if x < 8.0:
        return y0s(x)
    p, q = pqjy(x, 0)
    chi = x - math.pi / 4.0
    return math.sqrt(2.0 / (math.pi * x)) * (p * math.sin(chi) + q * math.cos(chi))


def y1f(x):
    if x < 8.0:
        return y1s(x)
    p, q = pqjy(x, 1)
    chi = x - math.pi / 2.0 - math.pi / 4.0
    return math.sqrt(2.0 / (math.pi * x)) * (p * math.sin(chi) + q * math.cos(chi))


def i0s(x):
    q = x * x / 4.0
    term = 1.0
    s = 1.0
    for k in range(1, 151):
        term *= q / (k * k)
        s += term
    return s


def i1s(x):
    q = x * x / 4.0
    term = 1.0
    s = 1.0
    for k in range(1, 151):
        term *= q / (k * (k + 1.0))
        s += term
    return 0.5 * x * s


def aser(x, nu, nterms, alt):
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


def i0f(x):
    ax = abs(x)
    if ax < 15.0:
        return i0s(x)
    return math.exp(ax) / math.sqrt(2.0 * math.pi * ax) * aser(ax, 0, 20, True)


def i1f(x):
    ax = abs(x)
    v = i1s(ax) if ax < 15.0 else math.exp(ax) / math.sqrt(2.0 * math.pi * ax) * aser(ax, 1, 20, True)
    return -v if x < 0.0 else v


def k0s(x):
    q = x * x / 4.0
    m = 1.0
    h = 0.0
    s = 0.0
    for k in range(1, 61):
        m *= q / (k * k)
        h += 1.0 / k
        s += h * m
    return -(math.log(x / 2.0) + EULER) * i0s(x) + s


def k1s(x):
    pw = x / 2.0
    h = 0.0
    s = 0.0
    for k in range(61):
        hp1 = h + 1.0 / (k + 1.0)
        s += (h + hp1) * pw
        h = hp1
        pw *= (x * x / 4.0) / ((k + 1.0) * (k + 2.0))
    return 1.0 / x + (math.log(x / 2.0) + EULER) * i1s(x) - 0.5 * s


def k0f(x):
    if x < 6.0:
        return k0s(x)
    return math.sqrt(math.pi / (2.0 * x)) * math.exp(-x) * aser(x, 0, 16, False)


def k1f(x):
    if x < 6.0:
        return k1s(x)
    return math.sqrt(math.pi / (2.0 * x)) * math.exp(-x) * aser(x, 1, 16, False)


def bjn(n, x):
    acc = 160.0
    iexp = 512
    if n == 0:
        return j0f(x)
    if n == 1:
        return j1f(x)
    ax = abs(x)
    if ax * ax <= 8.0 * 2.2250738585072014e-308:
        return 0.0
    if ax > n:
        tox = 2.0 / ax
        bjm = j0f(ax)
        bj = j1f(ax)
        for j in range(1, n):
            bjp = j * tox * bj - bjm
            bjm = bj
            bj = bjp
        ans = bj
    else:
        tox = 2.0 / ax
        m = 2 * ((n + int(math.sqrt(acc * n))) // 2)
        jsum = False
        bjp = 0.0
        bj = 1.0
        sm = 0.0
        ans = 0.0
        for j in range(m, 0, -1):
            bjm = j * tox * bj - bjp
            bjp = bj
            bj = bjm
            _, k = math.frexp(bj)
            if k > iexp:
                bj = math.ldexp(bj, -iexp)
                bjp = math.ldexp(bjp, -iexp)
                ans = math.ldexp(ans, -iexp)
                sm = math.ldexp(sm, -iexp)
            if jsum:
                sm += bj
            jsum = not jsum
            if j == n:
                ans = bjp
        sm = 2.0 * sm - bj
        ans /= sm
    return -ans if x < 0.0 and (n & 1) else ans


def byn(n, x):
    if n == 0:
        return y0f(x)
    if n == 1:
        return y1f(x)
    tox = 2.0 / x
    by = y1f(x)
    bym = y0f(x)
    for j in range(1, n):
        byp = j * tox * by - bym
        bym = by
        by = byp
    return by


def binf(n, x):
    acc = 200.0
    iexp = 512
    if n == 0:
        return i0f(x)
    if n == 1:
        return i1f(x)
    if x * x <= 8.0 * 2.2250738585072014e-308:
        return 0.0
    tox = 2.0 / abs(x)
    bip = 0.0
    bi = 1.0
    ans = 0.0
    for j in range(2 * (n + int(math.sqrt(acc * n))), 0, -1):
        bim = bip + j * tox * bi
        bip = bi
        bi = bim
        _, k = math.frexp(bi)
        if k > iexp:
            ans = math.ldexp(ans, -iexp)
            bi = math.ldexp(bi, -iexp)
            bip = math.ldexp(bip, -iexp)
        if j == n:
            ans = bip
    ans *= i0f(x) / bi
    return -ans if x < 0.0 and (n & 1) else ans


def bkn(n, x):
    if n == 0:
        return k0f(x)
    if n == 1:
        return k1f(x)
    tox = 2.0 / x
    bkm = k0f(x)
    bk = k1f(x)
    for j in range(1, n):
        bkp = bkm + j * tox * bk
        bkm = bk
        bk = bkp
    return bk


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    x = float(toks[2])
    if op == "JN":
        ans = bjn(n, x)
    elif op == "YN":
        ans = byn(n, x)
    elif op == "IN":
        ans = binf(n, x)
    else:
        ans = bkn(n, x)
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
