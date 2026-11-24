# Power spectrum estimation: windowed periodograms over segments
# (Spectreg), half-overlapping segments (Spectolap, incl. long-data
# accordion), and Slepian multitaper (filltable eigensolver).
# Reference: Press et al., Numerical Recipes 3e, Section 13.5
# (Spectreg/Spectolap/Slepian, vendoring realft+four1 from 12.2-12.3).
# Documented decisions: frequencies() is not output (closed form
# i*0.5/m); unknown window names flag; m must be a power of 2
# >= 1 (m = 1 flags via realft); SLEPIAN needs m >= 2 (its
# table build indexes u[3]); Newton breaks identically given
# identical libm-class inputs; SQR(x) is x*x.
# No online-judge problem found -- fixtures are self-generated
# (numpy/scipy oracle), no header link.
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


class Spectreg:
    def __init__(self, m, wtype):
        if m < 1 or (m & (m - 1)):
            raise BadN()
        self.m = m
        self.m2 = 2 * m
        self.nsum = 0
        self.specsum = [0.0] * (m + 1)
        self.wksp = [0.0] * (2 * m)
        self.wtype = wtype
        self.hanntab = None
        if wtype == 3:
            twopi = 8.0 * math.atan(1.0)
            self.hanntab = [0.5 * (1.0 - math.cos(i * twopi / (2 * m - 1.0)))
                            for i in range(2 * m)]

    def window(self, j, n):
        if self.wtype == 1:
            return 1.0 - abs(2.0 * j / (n - 1.0) - 1.0)
        if self.wtype == 2:
            t = 2.0 * j / (n - 1.0) - 1.0
            return 1.0 - t * t
        if self.wtype == 3:
            if n != self.m2:
                raise BadN()
            return self.hanntab[j]
        return 1.0

    def adddataseg(self, data):
        if len(data) != self.m2:
            raise BadN()
        sumw = 0.0
        for i in range(self.m2):
            w = self.window(i, self.m2)
            self.wksp[i] = w * data[i]
            sumw += w * w
        fac = 2.0 / (sumw * self.m2)
        realft(self.wksp, 1)
        self.specsum[0] += 0.5 * fac * self.wksp[0] * self.wksp[0]
        for i in range(1, self.m):
            self.specsum[i] += fac * (self.wksp[2 * i] * self.wksp[2 * i]
                                     + self.wksp[2 * i + 1] * self.wksp[2 * i + 1])
        self.specsum[self.m] += 0.5 * fac * self.wksp[1] * self.wksp[1]
        self.nsum += 1

    def spectrum(self):
        if self.nsum == 0:
            raise BadN()
        return [v / self.nsum for v in self.specsum]


class Spectolap(Spectreg):
    def __init__(self, m, wtype):
        super().__init__(m, wtype)
        self.first = True
        self.fullseg = [0.0] * (2 * m)

    def adddataseg(self, data):
        if len(data) != self.m:
            raise BadN()
        if self.first:
            for i in range(self.m):
                self.fullseg[i + self.m] = data[i]
            self.first = False
        else:
            for i in range(self.m):
                self.fullseg[i] = self.fullseg[i + self.m]
                self.fullseg[i + self.m] = data[i]
            super().adddataseg(self.fullseg)

    def addlongdata(self, data):
        nt = len(data)
        nk = (nt - 1) // self.m
        dl = (nt - self.m2) / (nk - 1.0) if nk > 1 else 0.0
        if nt < self.m2:
            raise BadN()
        for k in range(nk):
            noff = int(k * dl + 0.5)
            for i in range(self.m2):
                self.fullseg[i] = data[noff + i]
            super().adddataseg(self.fullseg)


class Slepian(Spectreg):
    def __init__(self, m, jres, kt):
        super().__init__(m, -1)
        if jres < 1 or kt >= 2 * jres:
            raise BadN()
        if m < 2:
            raise BadN()
        self.jres = jres
        self.kt = kt
        self.dpss = [[0.0] * self.m2 for _ in range(kt)]
        self.p = self.pp = self.d = self.dd = 0.0
        self.filltable()

    def renorm(self, n):
        self.p = math.ldexp(self.p, n)
        self.pp = math.ldexp(self.pp, n)
        self.d = math.ldexp(self.d, n)
        self.dd = math.ldexp(self.dd, n)

    def filltable(self):
        m2 = self.m2
        jres = self.jres
        EPS = 1.0e-10
        PI = 4.0 * math.atan(1.0)
        dg = [0.0] * m2
        dgg = [0.0] * m2
        gam = [0.0] * m2
        sup = [0.0] * (m2 - 1)
        sub = [0.0] * (m2 - 1)
        s0 = math.sin(jres * PI / m2)
        sw = 2.0 * s0 * s0
        t0 = m2 - 1.0
        dg[0] = 0.25 * (2 * m2 + sw * t0 * t0 - 1.0)
        for i in range(1, m2):
            t1 = m2 - 1.0 - 2 * i
            dg[i] = 0.25 * (sw * t1 * t1 + (2 * (m2 - i) - 1.0) * (2 * i + 1.0))
            sub[i - 1] = sup[i - 1] = -i * float(m2 - i) / 2.0
        xx = -0.10859 - 0.068762 / jres + 1.5692 * jres
        xold = xx + 0.47276 + 0.20273 / jres - 3.1387 * jres
        for k in range(self.kt):
            u = self.dpss[k]
            for _ in range(20):
                self.pp = 1.0
                self.p = dg[0] - xx
                self.dd = 0.0
                self.d = -1.0
                for j in range(1, m2):
                    ppp = self.pp
                    self.pp = self.p
                    ddd = self.dd
                    self.dd = self.d
                    s1 = sup[j - 1]
                    self.p = self.pp * (dg[j] - xx) - ppp * s1 * s1
                    self.d = -self.pp + self.dd * (dg[j] - xx) - ddd * s1 * s1
                    if abs(self.p) > 1.0e30:
                        self.renorm(-100)
                    elif abs(self.p) < 1.0e-30:
                        self.renorm(100)
                xnew = xx - self.p / self.d
                if abs(xx - xnew) < EPS * abs(xnew):
                    break
                xx = xnew
            xx = xnew - (xold - xnew)
            xold = xnew
            for i in range(m2):
                dgg[i] = dg[i] - xnew
            nl = m2 // 3
            dgg[nl] = 1.0
            ssup = sup[nl]
            ssub = sub[nl - 1]
            u[0] = sup[nl] = sub[nl - 1] = 0.0
            bet = dgg[0]
            for i in range(1, m2):
                gam[i] = sup[i - 1] / bet
                bet = dgg[i] - sub[i - 1] * gam[i]
                u[i] = ((1.0 if i == nl else 0.0) - sub[i - 1] * u[i - 1]) / bet
            for i in range(m2 - 2, -1, -1):
                u[i] -= gam[i + 1] * u[i + 1]
            sup[nl] = ssup
            sub[nl - 1] = ssub
            s = 0.0
            for i in range(m2):
                s += u[i] * u[i]
            s = math.sqrt(s) if u[3] > 0.0 else -math.sqrt(s)
            for i in range(m2):
                u[i] /= s

    def adddataseg(self, data):
        if len(data) != self.m2:
            raise BadN()
        save = self.hanntab
        for k in range(self.kt):
            self.hanntab = self.dpss[k]
            self.wtype = 3
            super().adddataseg(data)
        self.hanntab = save
        self.wtype = -1


def fmt6(v):
    o = v
    if abs(o) < 5e-7:
        o = 0.0
    return "%.6f" % (o + 0.0)


def wtype_of(w):
    return {"SQUARE": 0, "BARTLETT": 1, "WELCH": 2, "HANN": 3}.get(w, -1)


def emit_zeros(m):
    w = m + 1 if m >= 1 else 0
    parts = ["0.000000"] * w
    parts.append("1")
    print(" ".join(parts))


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "SLEPIAN":
        m = int(toks[1])
        jres = int(toks[2])
        kt = int(toks[3])
        k = int(toks[4])
        p = 5
        try:
            sp = Slepian(m, jres, kt)
            for _ in range(k):
                seg = [float(t) for t in toks[p:p + max(0, 2 * m)]]
                p += max(0, 2 * m)
                sp.adddataseg(seg)
            spec = sp.spectrum()
            parts = [fmt6(v) for v in spec]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            emit_zeros(m)
    elif op == "LONGDATA":
        m = int(toks[1])
        w = toks[2]
        nt = int(toks[3])
        data = [float(t) for t in toks[4:4 + max(0, nt)]]
        try:
            wt = wtype_of(w)
            if wt < 0:
                raise BadN()
            sp = Spectolap(m, wt)
            sp.addlongdata(data)
            spec = sp.spectrum()
            parts = [fmt6(v) for v in spec]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            emit_zeros(m)
    elif op == "PGRAM" or op == "OVERLAP":
        m = int(toks[1])
        w = toks[2]
        k = int(toks[3])
        seglen = max(0, 2 * m) if op == "PGRAM" else max(0, m)
        p = 4
        try:
            wt = wtype_of(w)
            if wt < 0:
                raise BadN()
            sp = Spectreg(m, wt) if op == "PGRAM" else Spectolap(m, wt)
            for _ in range(k):
                seg = [float(t) for t in toks[p:p + seglen]]
                p += seglen
                sp.adddataseg(seg)
            spec = sp.spectrum()
            parts = [fmt6(v) for v in spec]
            parts.append("0")
            print(" ".join(parts))
        except BadN:
            emit_zeros(m)


main()
