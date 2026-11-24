# N-dimensional complex FFT (forward and inverse) by successive
# one-dimensional Danielson-Lanczos passes with per-dimension
# bit-reversal.
# Reference: Press et al., Numerical Recipes 3e, Section 12.5 (fourn).
# Documented decisions: validity is tested on the product of the
# lengths only (ntot >= 2 a power of 2), exactly as the book does --
# for positive dims this is equivalent to testing each dim, and
# length-1 dims are faithful no-ops; the inverse is NOT normalized
# (returns ntot times the inverse); theta uses the book's integer
# division ifp2/ip1 and left-assoc isign*6.28.../k; the truncated
# literal 6.28318530717959 is used verbatim. Robustness: ntot is
# capped at 10^6 (beyond that, or non-positive dims, the flag-1
# path runs with output width clamped to 2M values).
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys

LIM = 1000000


class BadN(Exception):
    pass


def fourn(data, nn, isign):
    ndim = len(nn)
    ntot = 1
    for d in nn:
        ntot *= d
    if ntot < 2 or (ntot & (ntot - 1)):
        raise BadN()
    nprev = 1
    for idim in range(ndim - 1, -1, -1):
        n = nn[idim]
        nrem = ntot // (n * nprev)
        ip1 = nprev << 1
        ip2 = ip1 * n
        ip3 = ip2 * nrem
        i2rev = 0
        i2 = 0
        while i2 < ip2:
            if i2 < i2rev:
                i1 = i2
                while i1 < i2 + ip1 - 1:
                    i3 = i1
                    while i3 < ip3:
                        i3rev = i2rev + i3 - i2
                        t = data[i3]
                        data[i3] = data[i3rev]
                        data[i3rev] = t
                        t = data[i3 + 1]
                        data[i3 + 1] = data[i3rev + 1]
                        data[i3rev + 1] = t
                        i3 += ip2
                    i1 += 2
            ibit = ip2 >> 1
            while ibit >= ip1 and i2rev + 1 > ibit:
                i2rev -= ibit
                ibit >>= 1
            i2rev += ibit
            i2 += ip1
        ifp1 = ip1
        while ifp1 < ip2:
            ifp2 = ifp1 << 1
            theta = float(isign) * 6.28318530717959 / (ifp2 // ip1)
            wtemp = math.sin(0.5 * theta)
            wpr = -2.0 * wtemp * wtemp
            wpi = math.sin(theta)
            wr = 1.0
            wi = 0.0
            i3 = 0
            while i3 < ifp1:
                i1 = i3
                while i1 < i3 + ip1 - 1:
                    i2 = i1
                    while i2 < ip3:
                        k1 = i2
                        k2 = k1 + ifp1
                        tempr = wr * data[k2] - wi * data[k2 + 1]
                        tempi = wr * data[k2 + 1] + wi * data[k2]
                        data[k2] = data[k1] - tempr
                        data[k2 + 1] = data[k1 + 1] - tempi
                        data[k1] += tempr
                        data[k1 + 1] += tempi
                        i2 += ifp2
                    i1 += 2
                wtemp = wr
                wr = wtemp * wpr - wi * wpi + wr
                wi = wi * wpr + wtemp * wpi + wi
                i3 += ip1
            ifp1 = ifp2
        nprev *= n


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
    ndim = int(toks[1])
    nn = [int(t) for t in toks[2:2 + max(0, ndim)]]
    ntot = 1
    for d in nn:
        if d <= 0 or ntot > LIM:
            ntot = 0 if d <= 0 else LIM + 1
            break
        ntot *= d
        if ntot > LIM:
            ntot = LIM + 1
            break
    if ndim <= 0:
        ntot = 1
    valid = ntot >= 2 and ntot <= LIM and (ntot & (ntot - 1)) == 0
    nvals = 2 * ntot if valid else (0 if ntot <= 0 else min(2 * ntot, 2 * LIM))
    if op == "FFTND" or op == "IFFTND":
        isign = 1 if op == "FFTND" else -1
        base = 2 + max(0, ndim)
        data = [float(t) for t in toks[base:base + nvals]]
        try:
            if not valid:
                raise BadN()
            fourn(data, nn, isign)
            parts = [fmt6(v) for v in data]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            parts = ["0.000000"] * nvals
            parts.append("1")
            print(" ".join(parts))


main()
