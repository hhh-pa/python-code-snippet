# Coefficients of the interpolating polynomial (NR 3.5, polcof). Port of the C++ reference.
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def neville(xa, ya, m, x):
    c = list(ya[:m])
    d = list(ya[:m])
    dif = abs(x - xa[0])
    ns = 0
    for i in range(m):
        dift = abs(x - xa[i])
        if dift < dif:
            ns = i
            dif = dift
    y = ya[ns]
    ns -= 1
    for mm in range(1, m):
        for i in range(m - mm):
            ho = xa[i] - x
            hp = xa[i + mm] - x
            w = c[i + 1] - d[i]
            den = w / (ho - hp)
            d[i] = hp * den
            c[i] = ho * den
        if 2 * (ns + 1) < (m - mm):
            y += c[ns + 1]
        else:
            y += d[ns]
            ns -= 1
    return y


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    nums = [float(v) for v in toks[1:]]
    x = nums[:n]
    y = nums[n:2 * n]
    cof = []
    for _ in range(n):
        m = len(x)
        cj = neville(x, y, m, 0.0)
        cof.append(cj)
        xmin, k = 1.0e99, -1
        for i in range(m):
            if abs(x[i]) < xmin:
                xmin, k = abs(x[i]), i
            if x[i] != 0.0:
                y[i] = (y[i] - cj) / x[i]
        del x[k]
        del y[k]
    print(" ".join(fmt(v) for v in cof))


main()
