# Exponential integrals (NR 6.3).
import math
import sys

EULER = 0.577215664901533
EPS = 2.220446049250313e-16
BIG = 1.7976931348623157e308 * EPS
FPMIN = 1.0020841800044864e-292


def expint(n, x):
    maxit = 100
    nm1 = n - 1
    if n == 0:
        return math.exp(-x) / x
    if x == 0.0:
        return 1.0 / nm1
    if x > 1.0:
        b = x + n
        c = BIG
        d = 1.0 / b
        h = d
        for i in range(1, maxit + 1):
            a = -i * (nm1 + i)
            b += 2.0
            d = 1.0 / (a * d + b)
            c = b + a / c
            dl = c * d
            h *= dl
            if abs(dl - 1.0) <= EPS:
                break
        return h * math.exp(-x)
    ans = 1.0 / nm1 if nm1 != 0 else -math.log(x) - EULER
    fact = 1.0
    for i in range(1, maxit + 1):
        fact *= -x / i
        if i != nm1:
            dl = -fact / (i - nm1)
        else:
            psi = -EULER
            for ii in range(1, nm1 + 1):
                psi += 1.0 / ii
            dl = fact * (-math.log(x) + psi)
        ans += dl
        if abs(dl) < abs(ans) * EPS:
            break
    return ans


def eifunc(x):
    maxit = 100
    if x < FPMIN:
        return math.log(x) + EULER
    if x <= -math.log(EPS):
        sm = 0.0
        fact = 1.0
        for k in range(1, maxit + 1):
            fact *= x / k
            term = fact / k
            sm += term
            if term < EPS * sm:
                break
        return sm + math.log(x) + EULER
    sm = 0.0
    term = 1.0
    for k in range(1, maxit + 1):
        prev = term
        term *= k / x
        if term < EPS:
            break
        if term < prev:
            sm += term
        else:
            sm -= prev
            break
    return math.exp(x) * (1.0 + sm) / x


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "EN":
        ans = expint(int(toks[1]), float(toks[2]))
    else:
        ans = eifunc(float(toks[1]))
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
