# FFT of real-valued data by packing into half-length complex FFT
# (forward) with packed positive-frequency output, and its inverse.
# Reference: Press et al., Numerical Recipes 3e, Section 12.3 (realft,
# vendoring the four1 engine from 12.2).
# Documented decisions: the inverse is NOT normalized (returns n/2
# times the inverse -- "result must be multiplied by 2/n"); n must be
# a power of 2 >= 4 (four1 needs n/2 >= 2), anything else reports zero
# values with flag 1 (the book throws for n/2 invalid; odd n >= 5
# would silently misbehave there, so it is rejected here);
# the pi literal 3.141592653589793238 is used verbatim.
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
    n = int(toks[1])
    if op == "RFFT" or op == "IRFFT":
        isign = 1 if op == "RFFT" else -1
        data = [float(t) for t in toks[2:2 + max(0, n)]]
        try:
            realft(data, isign)
            parts = [fmt6(v) for v in data]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, n)
            parts.append("1")
            print(" ".join(parts))


main()
