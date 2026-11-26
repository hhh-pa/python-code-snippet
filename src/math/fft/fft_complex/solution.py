# Radix-2 complex FFT (forward and inverse) by the Danielson-Lanczos
# lemma with bit-reversal reorder and trigonometric recurrence.
# Reference: Press et al., Numerical Recipes 3e, Section 12.2 (four1).
# Documented decisions: the book's truncated literal 6.28318530717959
# is used verbatim (not full-precision 2*pi); the inverse transform is
# NOT normalized (returns N times the inverse, as the book does --
# "you do that yourself"); n < 2 or not a power of 2 throws in the
# book, reported here as zero values with flag 1.
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
    if op == "FFT" or op == "IFFT":
        isign = 1 if op == "FFT" else -1
        data = [float(t) for t in toks[2:2 + max(0, 2 * n)]]
        try:
            four1(data, n, isign)
            parts = [fmt6(v) for v in data]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * max(0, 2 * n)
            parts.append("1")
            print(" ".join(parts))


main()
