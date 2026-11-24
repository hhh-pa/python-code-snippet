# Cyclic convolution, deconvolution and correlation of real data
# via the packed real FFT.
# Reference: Press et al., Numerical Recipes 3e, Sections 13.2-13.3
# (convlv/correl, vendoring realft+four1 from 12.2-12.3).
# Documented decisions: n must be a power of 2 >= 4 (realft needs
# n/2 >= 2); m must be odd with 1 <= m <= n (the book would
# silently misbehave or index out of bounds outside this);
# deconvolution at an exact response zero, like any other book
# throw, reports zero values with flag 1; SQR(x) is x*x.
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys


class BadN(Exception):
    pass


def four1(data, n, isign):
    if n < 2 or (n & (n - 1)):
        raise BadN()
    nn = n << 1
    j = 1
    i = 1
    while i < nn:
        if j > i:
            t = data[j - 1]
            data[j - 1] = data[i - 1]
            data[i - 1] = t
            t = data[j]
            data[j] = data[i]
            data[i] = t
        m = n
        while m >= 2 and j > m:
            j -= m
            m >>= 1
        j += m
        i += 2
    mmax = 2
    while nn > mmax:
        istep = mmax << 1
        theta = float(isign) * (6.28318530717959 / mmax)
        wtemp = math.sin(0.5 * theta)
        wpr = -2.0 * wtemp * wtemp
        wpi = math.sin(theta)
        wr = 1.0
        wi = 0.0
        m = 1
        while m < mmax:
            i = m
            while i <= nn:
                j = i + mmax
                tempr = wr * data[j - 1] - wi * data[j]
                tempi = wr * data[j] + wi * data[j - 1]
                data[j - 1] = data[i - 1] - tempr
                data[j] = data[i] - tempi
                data[i - 1] += tempr
                data[i] += tempi
                i += istep
            wtemp = wr
            wr = wtemp * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
            m += 2
        mmax = istep


def realft(data, isign):
    n = len(data)
    if n < 4 or (n & (n - 1)):
        raise BadN()
    c1 = 0.5
    theta = 3.141592653589793238 / float(n >> 1)
    if isign == 1:
        c2 = -0.5
        four1(data, n >> 1, 1)
    else:
        c2 = 0.5
        theta = -theta
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    wr = 1.0 + wpr
    wi = wpi
    i = 1
    while i < (n >> 2):
        i1 = i + i
        i2 = 1 + i1
        i3 = n - i1
        i4 = 1 + i3
        h1r = c1 * (data[i1] + data[i3])
        h1i = c1 * (data[i2] - data[i4])
        h2r = -c2 * (data[i2] + data[i4])
        h2i = c2 * (data[i1] - data[i3])
        data[i1] = h1r + wr * h2r - wi * h2i
        data[i2] = h1i + wr * h2i + wi * h2r
        data[i3] = h1r - wr * h2r + wi * h2i
        data[i4] = -h1i + wr * h2i + wi * h2r
        wtemp = wr
        wr = wtemp * wpr - wi * wpi + wr
        wi = wi * wpr + wtemp * wpi + wi
        i += 1
    if isign == 1:
        h1r = data[0]
        data[0] = h1r + data[1]
        data[1] = h1r - data[1]
    else:
        h1r = data[0]
        data[0] = c1 * (h1r + data[1])
        data[1] = c1 * (h1r - data[1])
        four1(data, n >> 1, -1)


def convlv(data, respns, isign, ans):
    n = len(data)
    m = len(respns)
    if m < 1 or m > n or (m & 1) == 0:
        raise BadN()
    temp = [0.0] * n
    temp[0] = respns[0]
    i = 1
    while i < (m + 1) // 2:
        temp[i] = respns[i]
        temp[n - i] = respns[m - i]
        i += 1
    i = (m + 1) // 2
    while i < n - (m - 1) // 2:
        temp[i] = 0.0
        i += 1
    for i in range(n):
        ans[i] = data[i]
    realft(ans, 1)
    realft(temp, 1)
    no2 = n >> 1
    if isign == 1:
        i = 2
        while i < n:
            tmp = ans[i]
            ans[i] = (ans[i] * temp[i] - ans[i + 1] * temp[i + 1]) / no2
            ans[i + 1] = (ans[i + 1] * temp[i] + tmp * temp[i + 1]) / no2
            i += 2
        ans[0] = ans[0] * temp[0] / no2
        ans[1] = ans[1] * temp[1] / no2
    elif isign == -1:
        i = 2
        while i < n:
            mag2 = temp[i] * temp[i] + temp[i + 1] * temp[i + 1]
            if mag2 == 0.0:
                raise BadN()
            tmp = ans[i]
            ans[i] = (ans[i] * temp[i] + ans[i + 1] * temp[i + 1]) / mag2 / no2
            ans[i + 1] = (ans[i + 1] * temp[i] - tmp * temp[i + 1]) / mag2 / no2
            i += 2
        if temp[0] == 0.0 or temp[1] == 0.0:
            raise BadN()
        ans[0] = ans[0] / temp[0] / no2
        ans[1] = ans[1] / temp[1] / no2
    else:
        raise BadN()
    realft(ans, -1)


def correl(data1, data2, ans):
    n = len(data1)
    temp = [0.0] * n
    for i in range(n):
        ans[i] = data1[i]
        temp[i] = data2[i]
    realft(ans, 1)
    realft(temp, 1)
    no2 = n >> 1
    i = 2
    while i < n:
        tmp = ans[i]
        ans[i] = (ans[i] * temp[i] + ans[i + 1] * temp[i + 1]) / no2
        ans[i + 1] = (ans[i + 1] * temp[i] - tmp * temp[i + 1]) / no2
        i += 2
    ans[0] = ans[0] * temp[0] / no2
    ans[1] = ans[1] * temp[1] / no2
    realft(ans, -1)


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
    if op == "CONV" or op == "DECONV":
        n = int(toks[1])
        m = int(toks[2])
        data = [float(t) for t in toks[3:3 + max(0, n)]]
        respns = [float(t) for t in toks[3 + max(0, n):3 + max(0, n) + max(0, m)]]
        ans = [0.0] * max(0, n)
        try:
            convlv(data, respns, 1 if op == "CONV" else -1, ans)
            parts = [fmt6(v) for v in ans]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, n)
            parts.append("1")
            print(" ".join(parts))
    elif op == "CORR":
        n = int(toks[1])
        d1 = [float(t) for t in toks[2:2 + max(0, n)]]
        d2 = [float(t) for t in toks[2 + max(0, n):2 + 2 * max(0, n)]]
        ans = [0.0] * max(0, n)
        try:
            correl(d1, d2, ans)
            parts = [fmt6(v) for v in ans]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, n)
            parts.append("1")
            print(" ".join(parts))


main()
