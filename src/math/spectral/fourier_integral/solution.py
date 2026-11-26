# Fourier integrals I = Int_a^b exp(iwt)h(t) dt via FFT with cubic
# endpoint corrections (dftcor) and the illustrative driver (dftint)
# with polynomial interpolation of the DFT spectrum.
# Reference: Press et al., Numerical Recipes 3e, Section 13.10
# (dftcor/dftint, vendoring Poly_interp::rawinterp from 3.2 and
# realft+four1 from 12.2-12.3).
# Documented decisions: M = 64, NDFT = 1024, MPOL = 6 are fixed
# exactly as printed (the book calls them merely illustrative,
# but the printed program is what is extracted); h(t) arrives as
# M + 1 explicit samples, not a callback (memcof-style explicit
# input precedent); Poly_interp(xpol, ., MPOL).interp(en) is exactly
# rawinterp(0, en) because mm == n clamps locate/hunt to jlo = 0
# (fresh object, so cor = 0 takes the locate path); dftcor's throw
# (a >= b, th < 0, th > 3.1416) and rawinterp's den == 0 become
# value flags; divisions stay divisions (t2/45.0 etc. are NOT
# rewritten as multiplies).
# No online-judge problem found -- fixtures are self-generated
# (scipy/numpy oracle), no header link.
import math
import sys


class BadArgs(Exception):
    pass


def fmt6(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


def four1(data, n, isign):
    if n < 2 or (n & (n - 1)):
        raise BadArgs()
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
        theta = float(isign) * (6.28318530717959 / float(mmax))
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
                data[i - 1] = data[i - 1] + tempr
                data[i] = data[i] + tempi
                i += istep
            wtemp = wr
            wr = wtemp * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
            m += 2
        mmax = istep


def realft(data, isign):
    n = len(data)
    if n < 4 or (n & (n - 1)):
        raise BadArgs()
    c1 = 0.5
    half = n >> 1
    theta = 3.141592653589793238 / float(half)
    if isign == 1:
        c2 = -0.5
        four1(data, half, 1)
    else:
        c2 = 0.5
        theta = -theta
    wtemp = math.sin(0.5 * theta)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    wr = 1.0 + wpr
    wi = wpi
    for i in range(1, n >> 2):
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
    if isign == 1:
        h1r = data[0]
        data[0] = h1r + data[1]
        data[1] = h1r - data[1]
    else:
        h1r = data[0]
        data[0] = c1 * (h1r + data[1])
        data[1] = c1 * (h1r - data[1])
        four1(data, half, -1)


def poly_rawinterp(xa, ya, x):
    mm = 6
    ns = 0
    c = [0.0] * mm
    d = [0.0] * mm
    dif = abs(x - xa[0])
    for i in range(mm):
        dift = abs(x - xa[i])
        if dift < dif:
            ns = i
            dif = dift
        c[i] = ya[i]
        d[i] = ya[i]
    y = ya[ns]
    ns -= 1
    for m in range(1, mm):
        for i in range(mm - m):
            ho = xa[i] - x
            hp = xa[i + m] - x
            w = c[i + 1] - d[i]
            den = ho - hp
            if den == 0.0:
                raise BadArgs()
            den = w / den
            d[i] = hp * den
            c[i] = ho * den
        if 2 * (ns + 1) < (mm - m):
            y += c[ns + 1]
        else:
            y += d[ns]
            ns -= 1
    return y


def dftcor(w, delta, a, b, endpts):
    th = w * delta
    if a >= b or th < 0.0e0 or th > 3.1416e0:
        raise BadArgs()
    if abs(th) < 5.0e-2:
        t = th
        t2 = t * t
        t4 = t2 * t2
        t6 = t4 * t2
        corfac = 1.0 - (11.0 / 720.0) * t4 + (23.0 / 15120.0) * t6
        a0r = (-2.0 / 3.0) + t2 / 45.0 + (103.0 / 15120.0) * t4 - \
            (169.0 / 226800.0) * t6
        a1r = (7.0 / 24.0) - (7.0 / 180.0) * t2 + (5.0 / 3456.0) * t4 - \
            (7.0 / 259200.0) * t6
        a2r = (-1.0 / 6.0) + t2 / 45.0 - (5.0 / 6048.0) * t4 + t6 / 64800.0
        a3r = (1.0 / 24.0) - t2 / 180.0 + (5.0 / 24192.0) * t4 - t6 / 259200.0
        a0i = t * (2.0 / 45.0 + (2.0 / 105.0) * t2 - (8.0 / 2835.0) * t4 +
                   (86.0 / 467775.0) * t6)
        a1i = t * (7.0 / 72.0 - t2 / 168.0 + (11.0 / 72576.0) * t4 -
                   (13.0 / 5987520.0) * t6)
        a2i = t * (-7.0 / 90.0 + t2 / 210.0 - (11.0 / 90720.0) * t4 +
                   (13.0 / 7484400.0) * t6)
        a3i = t * (7.0 / 360.0 - t2 / 840.0 + (11.0 / 362880.0) * t4 -
                   (13.0 / 29937600.0) * t6)
    else:
        cth = math.cos(th)
        sth = math.sin(th)
        ctth = cth * cth - sth * sth
        stth = 2.0e0 * sth * cth
        th2 = th * th
        th4 = th2 * th2
        tmth2 = 3.0e0 - th2
        spth2 = 6.0e0 + th2
        sth4i = 1.0 / (6.0e0 * th4)
        tth4i = 2.0e0 * sth4i
        corfac = tth4i * spth2 * (3.0e0 - 4.0e0 * cth + ctth)
        a0r = sth4i * (-42.0e0 + 5.0e0 * th2 + spth2 * (8.0e0 * cth - ctth))
        a0i = sth4i * (th * (-12.0e0 + 6.0e0 * th2) + spth2 * stth)
        a1r = sth4i * (14.0e0 * tmth2 - 7.0e0 * spth2 * cth)
        a1i = sth4i * (30.0e0 * th - 5.0e0 * spth2 * sth)
        a2r = tth4i * (-4.0e0 * tmth2 + 2.0e0 * spth2 * cth)
        a2i = tth4i * (-12.0e0 * th + 2.0e0 * spth2 * sth)
        a3r = sth4i * (2.0e0 * tmth2 - spth2 * cth)
        a3i = sth4i * (6.0e0 * th - spth2 * sth)
    cl = a0r * endpts[0] + a1r * endpts[1] + a2r * endpts[2] + a3r * endpts[3]
    sl = a0i * endpts[0] + a1i * endpts[1] + a2i * endpts[2] + a3i * endpts[3]
    cr = a0r * endpts[7] + a1r * endpts[6] + a2r * endpts[5] + a3r * endpts[4]
    sr = -a0i * endpts[7] - a1i * endpts[6] - a2i * endpts[5] - a3i * endpts[4]
    arg = w * (b - a)
    c = math.cos(arg)
    s = math.sin(arg)
    corre = cl + c * cr - s * sr
    corim = sl + s * cr + c * sr
    return corre, corim, corfac


def dftint(a, b, w, h):
    m = 64
    ndft = 1024
    mpol = 6
    twopi = 6.283185307179586476
    if len(h) != m + 1:
        raise BadArgs()
    delta = (b - a) / m
    data = [0.0] * ndft
    for j in range(m + 1):
        data[j] = h[j]
    endpts = [0.0] * 8
    for j in range(4):
        endpts[j] = data[j]
        endpts[j + 4] = data[m - 3 + j]
    realft(data, 1)
    data[1] = 0.0
    en = w * delta * ndft / twopi + 1.0
    nn = min(max(int(en - 0.5 * mpol + 1.0), 1), ndft // 2 - mpol + 1)
    cpol = [0.0] * mpol
    spol = [0.0] * mpol
    xpol = [0.0] * mpol
    for j in range(mpol):
        cpol[j] = data[2 * nn - 2]
        spol[j] = data[2 * nn - 1]
        xpol[j] = float(nn)
        nn += 1
    cdft = poly_rawinterp(xpol, cpol, en)
    sdft = poly_rawinterp(xpol, spol, en)
    corre, corim, corfac = dftcor(w, delta, a, b, endpts)
    cdft *= corfac
    sdft *= corfac
    cdft += corre
    sdft += corim
    c = delta * math.cos(w * a)
    s = delta * math.sin(w * a)
    cosint = c * cdft - s * sdft
    sinint = s * cdft + c * sdft
    return cosint, sinint


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "DFTCOR":
        w = float(toks[1])
        delta = float(toks[2])
        a = float(toks[3])
        b = float(toks[4])
        endpts = [float(t) for t in toks[5:13]]
        try:
            corre, corim, corfac = dftcor(w, delta, a, b, endpts)
            print("%s %s %s 0" % (fmt6(corre), fmt6(corim), fmt6(corfac)))
        except BadArgs:
            print("0.000000 0.000000 0.000000 1")
    elif op == "DFTINT":
        a = float(toks[1])
        b = float(toks[2])
        w = float(toks[3])
        h = [float(t) for t in toks[4:69]]
        try:
            cosint, sinint = dftint(a, b, w, h)
            print("%s %s 0" % (fmt6(cosint), fmt6(sinint)))
        except BadArgs:
            print("0.000000 0.000000 1")


main()
