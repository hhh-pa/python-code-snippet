# FFT of real data in two and three dimensions by packing into a
# half-length complex FFT plus split/recombine with a Nyquist
# side array.
# Reference: Press et al., Numerical Recipes 3e, Section 12.6 (rlft3,
# vendoring the fourn engine from 12.5).
# Documented decisions: the inverse returns (n1*n2*n3/2) times the
# inverse; dims must be powers of 2 with nn1,nn2 >= 1 and nn3 >= 2
# (nn3 = 1 would index out of bounds in the book's inverse path),
# plus fourn's own ntot >= 2 check -- anything else reports zero
# values with flag 1; theta uses isign*(6.28.../nn3) as written;
# the truncated literal 6.28318530717959 is used verbatim.
# No online-judge problem found -- fixtures are self-generated
# (numpy oracle), no header link.
import math
import sys


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


def ispow2(n):
    return n >= 1 and (n & (n - 1)) == 0


def rlft3(data, speq, isign, nn1, nn2, nn3):
    if not ispow2(nn1) or not ispow2(nn2) or nn3 < 2 or (nn3 & (nn3 - 1)):
        raise BadN()

    def spq(a, b):
        return speq[a * 2 * nn2 + b]

    def setspq(a, b, v):
        speq[a * 2 * nn2 + b] = v

    c1 = 0.5
    c2 = -0.5 * isign
    theta = float(isign) * (6.28318530717959 / nn3)
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    nn = [nn1, nn2, nn3 >> 1]
    if isign == 1:
        fourn(data, nn, isign)
        k1 = 0
        for i1 in range(nn1):
            j2 = 0
            for i2 in range(nn2):
                setspq(i1, j2, data[k1])
                j2 += 1
                setspq(i1, j2, data[k1 + 1])
                j2 += 1
                k1 += nn3
    for i1 in range(nn1):
        j1 = nn1 - i1 if i1 != 0 else 0
        wr = 1.0
        wi = 0.0
        i3 = 0
        while i3 <= (nn3 >> 1):
            k1 = i1 * nn2 * nn3
            k3 = j1 * nn2 * nn3
            i2 = 0
            while i2 < nn2:
                if i3 == 0:
                    j2 = ((nn2 - i2) << 1) if i2 != 0 else 0
                    h1r = c1 * (data[k1] + spq(j1, j2))
                    h1i = c1 * (data[k1 + 1] - spq(j1, j2 + 1))
                    h2i = c2 * (data[k1] - spq(j1, j2))
                    h2r = -c2 * (data[k1 + 1] + spq(j1, j2 + 1))
                    data[k1] = h1r + h2r
                    data[k1 + 1] = h1i + h2i
                    setspq(j1, j2, h1r - h2r)
                    setspq(j1, j2 + 1, h2i - h1i)
                else:
                    j2 = nn2 - i2 if i2 != 0 else 0
                    j3 = nn3 - i3
                    k2 = k1 + i3
                    k4 = k3 + j2 * nn3 + j3
                    h1r = c1 * (data[k2] + data[k4])
                    h1i = c1 * (data[k2 + 1] - data[k4 + 1])
                    h2i = c2 * (data[k2] - data[k4])
                    h2r = -c2 * (data[k2 + 1] + data[k4 + 1])
                    data[k2] = h1r + wr * h2r - wi * h2i
                    data[k2 + 1] = h1i + wr * h2i + wi * h2r
                    data[k4] = h1r - wr * h2r + wi * h2i
                    data[k4 + 1] = -h1i + wr * h2i + wi * h2r
                i2 += 1
                k1 += nn3
            wtemp = wr
            wr = wtemp * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
            i3 += 2
    if isign == -1:
        fourn(data, nn, isign)


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def clamp2m(v):
    if v <= 0:
        return 0
    return 2000000 if v > 2000000 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    is2d = op == "RFFT2D" or op == "IRFFT2D"
    is3d = op == "RFFT3D" or op == "IRFFT3D"
    if not is2d and not is3d:
        return
    n1, n2, n3 = 1, 1, 1
    if is2d:
        n2 = int(toks[1])
        n3 = int(toks[2])
        base = 3
    else:
        n1 = int(toks[1])
        n2 = int(toks[2])
        n3 = int(toks[3])
        base = 4
    full_data = 0 if (n1 <= 0 or n2 <= 0 or n3 <= 0) else n1 * n2 * n3
    full_speq = 0 if (n1 <= 0 or n2 <= 0) else n1 * 2 * n2
    half3 = (n3 >> 1) if n3 >= 2 else 0
    ntot = 0 if (n1 <= 0 or n2 <= 0) else n1 * n2 * half3
    valid = ispow2(n1) and ispow2(n2) and n3 >= 2 and (n3 & (n3 - 1)) == 0 \
        and full_data <= 2000000 and full_speq <= 2000000 \
        and ntot >= 2 and (ntot & (ntot - 1)) == 0
    ndata = full_data if valid else clamp2m(full_data)
    nspeq = full_speq if valid else clamp2m(full_speq)
    inverse = op == "IRFFT2D" or op == "IRFFT3D"
    data = [float(t) for t in toks[base:base + ndata]]
    speq = [0.0] * nspeq
    if inverse:
        speq = [float(t) for t in toks[base + ndata:base + ndata + nspeq]]
    try:
        if not valid:
            raise BadN()
        rlft3(data, speq, -1 if inverse else 1, n1, n2, n3)
        parts = [fmt6(v) for v in data]
        if not inverse:
            parts += [fmt6(v) for v in speq]
        parts.append("0")
        print(" ".join(parts))
    except BadN:
        w = ndata if inverse else ndata + nspeq
        parts = ["0.000000"] * w
        parts.append("1")
        print(" ".join(parts))


main()
