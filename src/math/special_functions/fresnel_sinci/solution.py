# Fresnel and cosine/sine integrals (NR 6.8).
import math
import sys


def cxadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cxsub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cxmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cxdiv(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def frenel(x):
    maxit = 100
    piby2 = math.pi / 2.0
    xmin = 1.5
    eps = 2.220446049250313e-16
    fpmin = 2.2250738585072014e-308
    big = 1.7976931348623157e308 * eps
    ax = abs(x)
    if ax < math.sqrt(fpmin):
        cs = (ax, 0.0)
    elif ax <= xmin:
        sm = 0.0
        sums = 0.0
        sumc = ax
        sign = 1.0
        fact = piby2 * ax * ax
        odd = True
        term = ax
        n = 3
        for k in range(1, maxit + 1):
            term *= fact / k
            sm += sign * term / n
            test = abs(sm) * eps
            if odd:
                sign = -sign
                sums = sm
                sm = sumc
            else:
                sumc = sm
                sm = sums
            if term < test:
                break
            odd = not odd
            n += 2
        cs = (sumc, sums)
    else:
        pix2 = math.pi * ax * ax
        b = [1.0, -pix2]
        cc = [big, 0.0]
        d = cxdiv((1.0, 0.0), tuple(b))
        h = d
        n = -1
        for k in range(2, maxit + 1):
            n += 2
            a = -n * (n + 1)
            b[0] += 4.0
            d = cxdiv((1.0, 0.0), cxadd((a * d[0], a * d[1]), tuple(b)))
            cc = cxadd(tuple(b), cxdiv((a, 0.0), tuple(cc)))
            dl = cxmul(tuple(cc), d)
            h = cxmul(h, dl)
            if abs(dl[0] - 1.0) + abs(dl[1]) <= eps:
                break
        h = cxmul(h, (ax, -ax))
        e = (math.cos(0.5 * pix2), math.sin(0.5 * pix2))
        t = cxsub((1.0, 0.0), cxmul(e, h))
        cs = cxmul((0.5, 0.5), t)
    if x < 0.0:
        cs = (-cs[0], -cs[1])
    return cs


def cisi(x):
    maxit = 100
    euler = 0.577215664901533
    piby2 = 1.570796326794897
    tmin = 2.0
    eps = 2.220446049250313e-16
    fpmin = 2.2250738585072014e-308 * 4.0
    big = 1.7976931348623157e308 * eps
    t = abs(x)
    if t == 0.0:
        return (-big, 0.0)
    if t > tmin:
        b = [1.0, t]
        c = [big, 0.0]
        d = cxdiv((1.0, 0.0), tuple(b))
        h = d
        for i in range(1, maxit):
            a = -i * i
            b[0] += 2.0
            d = cxdiv((1.0, 0.0), cxadd((a * d[0], a * d[1]), tuple(b)))
            c = cxadd(tuple(b), cxdiv((a, 0.0), tuple(c)))
            dl = cxmul(tuple(c), d)
            h = cxmul(h, dl)
            if abs(dl[0] - 1.0) + abs(dl[1]) <= eps:
                break
        h = cxmul((math.cos(t), -math.sin(t)), h)
        cs = (-h[0], h[1] + piby2)
    else:
        if t < math.sqrt(fpmin):
            sumc = 0.0
            sums = t
        else:
            sm = 0.0
            sign = 1.0
            fact = 1.0
            sc = 0.0
            ss = 0.0
            odd = True
            for k in range(1, maxit + 1):
                fact *= t / k
                term = fact / k
                sm += sign * term
                err = term / abs(sm)
                if odd:
                    sign = -sign
                    ss = sm
                    sm = sc
                else:
                    sc = sm
                    sm = ss
                if err < eps:
                    break
                odd = not odd
            sumc = sc
            sums = ss
        cs = (sumc + math.log(t) + euler, sums)
    if x < 0.0:
        cs = (cs[0], -cs[1])
    return cs


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    x = float(toks[1])
    ans = frenel(x) if op == "FRESNEL" else cisi(x)
    r, im = ans
    if abs(r) < 5e-7:
        r = 0.0
    if abs(im) < 5e-7:
        im = 0.0
    sys.stdout.write("%.6f %.6f\n" % (r + 0.0, im + 0.0))


main()
