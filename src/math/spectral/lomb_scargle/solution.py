# Lomb-Scargle periodogram for unevenly sampled data: direct
# O(N^2) least-squares fit (period) and the FFT-based fast
# approximation with extirpolation (fasper/spread).
# Reference: Press et al., Numerical Recipes 3e, Section 13.9
# (period/fasper/spread, vendoring avevar from 14.2 and
# realft+four1 from 12.2-12.3).
# Documented decisions: n >= 2 enforced (n = 1 makes avevar's
# variance NaN, n = 0 overruns); nout must satisfy
# 1 <= nout <= 131072 and fasper's nfreq <= 2^20 (robustness
# caps on ofac/hifac); period keeps the LAST frequency on ties
# (>=), fasper the FIRST (>), exactly as the book; abscissas
# must span a positive range (xdif = 0 is unguarded garbage
# in the book); exact-zero variance flags (the book throws).
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


def avevar(data):
    n = len(data)
    if n < 2:
        raise BadN()
    ave = 0.0
    for j in range(n):
        ave += data[j]
    ave /= n
    var = 0.0
    ep = 0.0
    for j in range(n):
        s = data[j] - ave
        ep += s
        var += s * s
    var = (var - ep * ep / n) / (n - 1)
    return (ave, var)


def period(x, y, ofac, hifac):
    n = len(x)
    if n < 2 or ofac <= 0.0 or hifac <= 0.0:
        raise BadN()
    noutd = 0.5 * ofac * hifac * n
    if not 1.0 <= noutd <= 131072.0:
        raise BadN()
    nout = int(noutd)
    px = [0.0] * nout
    py = [0.0] * nout
    ave, var = avevar(y)
    if var == 0.0:
        raise BadN()
    xmin = min(x)
    xmax = max(x)
    xdif = xmax - xmin
    if not xdif > 0.0:
        raise BadN()
    TWOPI = 6.283185307179586476
    wr = [0.0] * n
    wi = [0.0] * n
    wpr = [0.0] * n
    wpi = [0.0] * n
    jmax = 0
    pymax = 0.0
    xave = 0.5 * (xmin + xmax)
    p0 = 1.0 / (xdif * ofac)
    for j in range(n):
        wpi0 = TWOPI * ((x[j] - xave) * p0)
        s = math.sin(0.5 * wpi0)
        wpr[j] = -2.0 * s * s
        wpi[j] = math.sin(wpi0)
        wr[j] = math.cos(wpi0)
        wi[j] = math.sin(wpi0)
    for i in range(nout):
        pnow = (i + 1) / (ofac * xdif)
        px[i] = pnow
        sumsh = 0.0
        sumc = 0.0
        for j in range(n):
            c = math.cos(pnow * TWOPI * (x[j] - xave))
            s = math.sin(pnow * TWOPI * (x[j] - xave))
            sumsh += s * c
            sumc += (c - s) * (c + s)
        wtau = 0.5 * math.atan2(2.0 * sumsh, sumc)
        swtau = math.sin(wtau)
        cwtau = math.cos(wtau)
        sums = 0.0
        sumc = 0.0
        sumsy = 0.0
        sumcy = 0.0
        for j in range(n):
            ss = wr[j] * swtau - cwtau * wi[j]
            cc = wr[j] * cwtau + swtau * wi[j]
            sums += ss * ss
            sumc += cc * cc
            yy = y[j] - ave
            sumsy += yy * ss
            sumcy += yy * cc
            wtemp = wr[j]
            wr[j] = wtemp * wpr[j] - wi[j] * wpi[j] + wr[j]
            wi[j] = wi[j] * wpr[j] + wtemp * wpi[j] + wi[j]
        py[i] = 0.5 * (sumcy * sumcy / sumc + sumsy * sumsy / sums) / var
        if py[i] >= pymax:
            pymax = py[i]
            jmax = i
    expy = math.exp(-pymax)
    effm = 2.0 * nout / ofac
    prob = effm * expy
    if prob > 0.01:
        prob = 1.0 - (1.0 - expy) ** effm
    return (px, py, jmax, prob)


def spread(y, yy, x, m):
    nfac = [0, 1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
    if m > 10:
        raise BadN()
    n = len(yy)
    ix = int(x)
    if x == float(ix):
        yy[ix - 1] += y
    else:
        t = x - 0.5 * m
        ilo = min(max(int(t), 0), n - m)
        ihi = ilo + m
        nden = nfac[m]
        fac = x - ilo - 1
        for j in range(ilo + 1, ihi):
            fac *= x - j - 1
        yy[ihi - 1] += y * fac / (nden * (x - ihi))
        for j in range(ihi - 1, ilo, -1):
            nden = (nden // (j - ilo)) * (j - ihi)
            yy[j - 1] += y * fac / (nden * (x - j))


def fasper(x, y, ofac, hifac):
    n = len(x)
    if n < 2 or ofac <= 0.0 or hifac <= 0.0:
        raise BadN()
    noutd = 0.5 * ofac * hifac * n
    if not 1.0 <= noutd <= 131072.0:
        raise BadN()
    nout = int(noutd)
    nfreqt = ofac * hifac * n * 4
    nfreq = 64
    while nfreq < nfreqt:
        nfreq <<= 1
        if nfreq > 1048576:
            raise BadN()
    px = [0.0] * nout
    py = [0.0] * nout
    nwk = nfreq << 1
    wk1 = [0.0] * nwk
    wk2 = [0.0] * nwk
    ave, var = avevar(y)
    if var == 0.0:
        raise BadN()
    xmin = min(x)
    xmax = max(x)
    xdif = xmax - xmin
    if not xdif > 0.0:
        raise BadN()
    fac = nwk / (xdif * ofac)
    fndim = float(nwk)
    df = 1.0 / (xdif * ofac)
    pmax = -1.0
    jmax = 0
    for j in range(n):
        ck = math.fmod((x[j] - xmin) * fac, fndim)
        ckk = 2.0 * ck
        ck += 1.0
        ckk = math.fmod(ckk, fndim)
        ckk += 1.0
        spread(y[j] - ave, wk1, ck, 4)
        spread(1.0, wk2, ckk, 4)
    realft(wk1, 1)
    realft(wk2, 1)
    k = 2
    for j in range(nout):
        hypo = math.sqrt(wk2[k] * wk2[k] + wk2[k + 1] * wk2[k + 1])
        hc2wt = 0.5 * wk2[k] / hypo
        hs2wt = 0.5 * wk2[k + 1] / hypo
        cwt = math.sqrt(0.5 + hc2wt)
        s = math.sqrt(0.5 - hc2wt)
        swt = s if hs2wt >= 0.0 else -s
        den = 0.5 * n + hc2wt * wk2[k] + hs2wt * wk2[k + 1]
        t1 = cwt * wk1[k] + swt * wk1[k + 1]
        cterm = t1 * t1 / den
        t2 = cwt * wk1[k + 1] - swt * wk1[k]
        sterm = t2 * t2 / (n - den)
        px[j] = (j + 1) * df
        py[j] = (cterm + sterm) / (2.0 * var)
        if py[j] > pmax:
            pmax = py[j]
            jmax = j
        k += 2
    expy = math.exp(-pmax)
    effm = 2.0 * nout / ofac
    prob = effm * expy
    if prob > 0.01:
        prob = 1.0 - (1.0 - expy) ** effm
    return (px, py, jmax, prob)


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
    if op == "LOMB" or op == "FASTLOMB":
        n = int(toks[1])
        x = [float(t) for t in toks[2:2 + max(0, n)]]
        y = [float(t) for t in toks[2 + max(0, n):2 + 2 * max(0, n)]]
        ofac = float(toks[2 + 2 * max(0, n)])
        hifac = float(toks[3 + 2 * max(0, n)])
        try:
            if op == "LOMB":
                px, py, jmax, prob = period(x, y, ofac, hifac)
            else:
                px, py, jmax, prob = fasper(x, y, ofac, hifac)
            parts = [fmt6(v) for v in px]
            parts += [fmt6(v) for v in py]
            parts.append(str(jmax))
            parts.append(fmt6(prob))
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            nout = 0
            if n >= 2 and ofac > 0.0 and hifac > 0.0:
                nd = 0.5 * ofac * hifac * n
                if nd >= 1.0:
                    nout = int(nd) if nd <= 131072.0 else 131072
            parts = ["0.000000"] * (2 * nout)
            parts += ["0", "0.000000", "1"]
            print(" ".join(parts))


main()
