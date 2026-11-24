# Fast sine and cosine transforms via the real FFT plus
# auxiliary-array packing and odd/even unfolding.
# Reference: Press et al., Numerical Recipes 3e, Section 12.4
# (sinft/cosft1/cosft2, vendoring realft+four1 from 12.2-12.3).
# Documented decisions: sinft/cosft1 are self-inverse up to a
# factor (applying twice gives n/2 times the input -- "output
# should be multiplied by 2/n" for inverse use); cosft2 inverse
# likewise returns n/2 times the inverse; sizes must be powers
# of 2 >= 4 (realft needs n/2 >= 2), anything else reports zero
# values with flag 1; sinft forces y[0] = 0 (f_0 is identically
# 0), ignoring input y[0]; the pi literal 3.141592653589793238
# is used verbatim.
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys

PI = 3.141592653589793238


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
    theta = PI / float(n >> 1)
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


def sinft(y):
    n = len(y)
    if n < 4 or (n & (n - 1)):
        raise BadN()
    wi = 0.0
    wr = 1.0
    theta = PI / float(n)
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    y[0] = 0.0
    j = 1
    while j < (n >> 1) + 1:
        wtemp = wr
        wr = wtemp * wpr - wi * wpi + wr
        wi = wi * wpr + wtemp * wpi + wi
        y1 = wi * (y[j] + y[n - j])
        y2 = 0.5 * (y[j] - y[n - j])
        y[j] = y1 + y2
        y[n - j] = y1 - y2
        j += 1
    realft(y, 1)
    y[0] *= 0.5
    s = 0.0
    y[1] = 0.0
    j = 0
    while j < n - 1:
        s += y[j]
        y[j] = y[j + 1]
        y[j + 1] = s
        j += 2


def cosft1(y):
    n = len(y) - 1
    if n < 4 or (n & (n - 1)):
        raise BadN()
    wi = 0.0
    wr = 1.0
    yy = [0.0] * n
    theta = PI / n
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    s = 0.5 * (y[0] - y[n])
    yy[0] = 0.5 * (y[0] + y[n])
    j = 1
    while j < n // 2:
        wtemp = wr
        wr = wtemp * wpr - wi * wpi + wr
        wi = wi * wpr + wtemp * wpi + wi
        y1 = 0.5 * (y[j] + y[n - j])
        y2 = y[j] - y[n - j]
        yy[j] = y1 - wi * y2
        yy[n - j] = y1 + wi * y2
        s += wr * y2
        j += 1
    yy[n // 2] = y[n // 2]
    realft(yy, 1)
    for j in range(n):
        y[j] = yy[j]
    y[n] = y[1]
    y[1] = s
    j = 3
    while j < n:
        s += y[j]
        y[j] = s
        j += 2


def cosft2(y, isign):
    n = len(y)
    if n < 4 or (n & (n - 1)):
        raise BadN()
    wi = 0.0
    wr = 1.0
    theta = 0.5 * PI / n
    wr1 = math.cos(theta)
    wi1 = math.sin(theta)
    wpr = -2.0 * wi1 * wi1
    wpi = math.sin(2.0 * theta)
    if isign == 1:
        i = 0
        while i < n // 2:
            y1 = 0.5 * (y[i] + y[n - 1 - i])
            y2 = wi1 * (y[i] - y[n - 1 - i])
            y[i] = y1 + y2
            y[n - 1 - i] = y1 - y2
            wtemp = wr1
            wr1 = wtemp * wpr - wi1 * wpi + wr1
            wi1 = wi1 * wpr + wtemp * wpi + wi1
            i += 1
        realft(y, 1)
        i = 2
        while i < n:
            wtemp = wr
            wr = wtemp * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
            y1 = y[i] * wr - y[i + 1] * wi
            y2 = y[i + 1] * wr + y[i] * wi
            y[i] = y1
            y[i + 1] = y2
            i += 2
        s = 0.5 * y[1]
        i = n - 1
        while i > 0:
            s1 = s
            s += y[i]
            y[i] = s1
            i -= 2
    elif isign == -1:
        ytemp = y[n - 1]
        i = n - 1
        while i > 2:
            y[i] = y[i - 2] - y[i]
            i -= 2
        y[1] = 2.0 * ytemp
        i = 2
        while i < n:
            wtemp = wr
            wr = wtemp * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
            y1 = y[i] * wr + y[i + 1] * wi
            y2 = y[i + 1] * wr - y[i] * wi
            y[i] = y1
            y[i + 1] = y2
            i += 2
        realft(y, -1)
        i = 0
        while i < n // 2:
            y1 = y[i] + y[n - 1 - i]
            y2 = (0.5 / wi1) * (y[i] - y[n - 1 - i])
            y[i] = 0.5 * (y1 + y2)
            y[n - 1 - i] = 0.5 * (y1 - y2)
            wtemp = wr1
            wr1 = wtemp * wpr - wi1 * wpi + wr1
            wi1 = wi1 * wpr + wtemp * wpi + wi1
            i += 1


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def emit(vals, ok):
    if ok:
        return " ".join([fmt6(v) for v in vals] + ["0"])
    return " ".join(["0.000000"] * len(vals) + ["1"])


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    if op == "SINFT" or op == "COSFT2F" or op == "COSFT2I":
        y = [float(t) for t in toks[2:2 + max(0, n)]]
        try:
            if op == "SINFT":
                sinft(y)
            elif op == "COSFT2F":
                cosft2(y, 1)
            else:
                cosft2(y, -1)
            print(emit(y, True))
        except BadN:
            print(emit(y, False))
    elif op == "COSFT1":
        y = [float(t) for t in toks[2:2 + max(0, n + 1)]]
        try:
            cosft1(y)
            print(emit(y, True))
        except BadN:
            print(emit(y, False))


main()
