# Non-uniform deviates (NR 7.3).
import math
import sys

M64 = 0xFFFFFFFFFFFFFFFF

GCOF = [57.1562356658629235, -59.5979603554754912, 14.1360979747417471,
        -0.491913816097620199, 0.339946499848118887e-4, 0.465236289270485756e-4,
        -0.983744753048795646e-4, 0.158088703224912494e-3, -0.210264441724104883e-3,
        0.217439618115212643e-3, -0.164318106536763890e-3, 0.844182239838527433e-4,
        -0.261908384015814087e-4, 0.368991826595316234e-5]


def gammln(xx):
    y = xx
    x = xx
    tmp = x + 5.2421875000000000
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 0.999999999999997092
    for j in range(14):
        y += 1.0
        ser += GCOF[j] / y
    return tmp + math.log(2.5066282746310005 * ser / x)


class Ran:
    def __init__(self, j):
        self.v = 4101842887655102017
        self.w = 1
        self.u = j ^ self.v
        self.int64()
        self.v = self.u
        self.int64()
        self.w = self.v
        self.int64()

    def int64(self):
        self.u = (self.u * 2862933555777941757 + 7046029254386353087) & M64
        self.v ^= self.v >> 17
        self.v ^= (self.v << 31) & M64
        self.v ^= self.v >> 8
        self.w = (4294957665 * (self.w & 0xFFFFFFFF) + (self.w >> 32)) & M64
        x = self.u ^ ((self.u << 21) & M64)
        x ^= x >> 35
        x ^= (x << 4) & M64
        return ((x + self.v) & M64) ^ self.w

    def doub(self):
        return 5.42101086242752217e-20 * float(self.int64())


class Expondev(Ran):
    def __init__(self, bet, i):
        super().__init__(i)
        self.beta = bet

    def dev(self):
        while True:
            u = self.doub()
            if u != 0.0:
                return -math.log(u) / self.beta


class Logisticdev(Ran):
    def __init__(self, mu, sig, i):
        super().__init__(i)
        self.mu = mu
        self.sig = sig

    def dev(self):
        while True:
            u = self.doub()
            if u * (1.0 - u) != 0.0:
                return self.mu + 0.551328895421792050 * self.sig * math.log(u / (1.0 - u))


class Cauchydev(Ran):
    def __init__(self, mu, sig, i):
        super().__init__(i)
        self.mu = mu
        self.sig = sig

    def dev(self):
        while True:
            v1 = 2.0 * self.doub() - 1.0
            v2 = self.doub()
            if not (v1 * v1 + v2 * v2 >= 1.0 or v2 == 0.0):
                return self.mu + self.sig * v1 / v2


class Normaldev(Ran):
    def __init__(self, mu, sig, i):
        super().__init__(i)
        self.mu = mu
        self.sig = sig

    def dev(self):
        while True:
            u = self.doub()
            v = 1.7156 * (self.doub() - 0.5)
            x = u - 0.449871
            y = abs(v) + 0.386595
            q = x * x + y * (0.19600 * y - 0.25472 * x)
            if not (q > 0.27597 and (q > 0.27846 or v * v > -4.0 * math.log(u) * u * u)):
                return self.mu + self.sig * v / u


class NormaldevBM(Ran):
    def __init__(self, mu, sig, i):
        super().__init__(i)
        self.mu = mu
        self.sig = sig
        self.storedval = 0.0

    def dev(self):
        if self.storedval == 0.0:
            while True:
                v1 = 2.0 * self.doub() - 1.0
                v2 = 2.0 * self.doub() - 1.0
                rsq = v1 * v1 + v2 * v2
                if not (rsq >= 1.0 or rsq == 0.0):
                    break
            fac = math.sqrt(-2.0 * math.log(rsq) / rsq)
            self.storedval = v1 * fac
            return self.mu + self.sig * v2 * fac
        fac = self.storedval
        self.storedval = 0.0
        return self.mu + self.sig * fac


class Gammadev(Normaldev):
    def __init__(self, alph, bet, i):
        super().__init__(0.0, 1.0, i)
        self.oalph = alph
        if alph < 1.0:
            alph += 1.0
        self.alph = alph
        self.bet = bet
        self.a1 = alph - 1.0 / 3.0
        self.a2 = 1.0 / math.sqrt(9.0 * self.a1)

    def dev(self):
        while True:
            while True:
                x = Normaldev.dev(self)
                v = 1.0 + self.a2 * x
                if v > 0.0:
                    break
            v = v * v * v
            u = self.doub()
            if not (u > 1.0 - 0.331 * x * x * x * x
                    and math.log(u) > 0.5 * x * x + self.a1 * (1.0 - v + math.log(v))):
                break
        if self.alph == self.oalph:
            return self.a1 * v / self.bet
        while True:
            u = self.doub()
            if u != 0.0:
                return math.pow(u, 1.0 / self.oalph) * self.a1 * v / self.bet


class Poissondev(Ran):
    def __init__(self, lam, i):
        super().__init__(i)
        self.lam = lam
        self.logfact = [-1.0] * 1024
        self.lambold = -1.0

    def dev(self):
        lam = self.lam
        if lam < 5.0:
            if lam != self.lambold:
                self.lamexp = math.exp(-lam)
            k = -1
            t = 1.0
            while True:
                k += 1
                t *= self.doub()
                if not t > self.lamexp:
                    break
        else:
            if lam != self.lambold:
                self.sqlam = math.sqrt(lam)
                self.loglam = math.log(lam)
            while True:
                u = 0.64 * self.doub()
                v = -0.68 + 1.28 * self.doub()
                if u == 0.0:
                    continue
                if lam > 13.5:
                    v2 = v * v
                    if v >= 0.0:
                        if v2 > 6.5 * u * (0.64 - u) * (u + 0.2):
                            continue
                    elif v2 > 9.6 * u * (0.66 - u) * (u + 0.07):
                        continue
                kf = math.floor(self.sqlam * (v / u) + lam + 0.5)
                if kf < 0 or kf >= 9223372036854775808:
                    continue
                k = kf
                u2 = u * u
                if lam > 13.5:
                    if v >= 0.0:
                        if v2 < 15.2 * u2 * (0.61 - u) * (0.8 - u):
                            break
                    elif v2 < 6.76 * u2 * (0.62 - u) * (1.4 - u):
                        break
                else:
                    pass
                if k < 1024:
                    if self.logfact[k] < 0.0:
                        self.logfact[k] = gammln(k + 1.0)
                    lfac = self.logfact[k]
                else:
                    lfac = gammln(k + 1.0)
                p = self.sqlam * math.exp(-lam + k * self.loglam - lfac)
                if u2 < p:
                    break
        self.lambold = lam
        return k


class Binomialdev(Ran):
    def __init__(self, nn, ppp, i):
        super().__init__(i)
        self.pp = ppp
        self.n = nn
        self.pb = self.p = ppp if ppp <= 0.5 else 1.0 - ppp
        if nn <= 64:
            self.uz = 0
            self.uo = M64
            self.rltp = 0
            self.pbits = []
            pb = self.pb
            for _ in range(5):
                pb *= 2.0
                self.pbits.append(1 & int(pb))
            self.pb = pb - math.floor(pb)
            self.swch = 0
        elif nn * self.p < 30.0:
            self.cdf = [0.0] * 64
            self.cdf[0] = math.exp(nn * math.log(1 - self.p))
            for j in range(1, 64):
                self.cdf[j] = self.cdf[j - 1] + math.exp(
                    gammln(nn + 1.0) - gammln(j + 1.0) - gammln(nn - j + 1.0)
                    + j * math.log(self.p) + (nn - j) * math.log(1.0 - self.p))
            self.swch = 1
        else:
            self.np = nn * self.p
            self.glnp = gammln(nn + 1.0)
            self.plog = math.log(self.p)
            self.pclog = math.log(1.0 - self.p)
            self.sq = math.sqrt(self.np * (1.0 - self.p))
            self.logfact = [0.0] * 1024
            if nn < 1024:
                for j in range(nn + 1):
                    self.logfact[j] = gammln(j + 1.0)
            self.swch = 2

    def dev(self):
        if self.swch == 0:
            unfin = self.uo
            rltp = self.rltp
            for j in range(5):
                diff = unfin & (self.int64() ^ (self.uo if self.pbits[j] else self.uz))
                if self.pbits[j]:
                    rltp |= diff
                else:
                    rltp &= ~diff & M64
                unfin &= ~diff & M64
            self.rltp = rltp
            k = 0
            for _ in range(self.n):
                if unfin & 1:
                    if self.doub() < self.pb:
                        k += 1
                elif rltp & 1:
                    k += 1
                unfin >>= 1
                rltp >>= 1
        elif self.swch == 1:
            y = self.doub()
            kl = -1
            k = 64
            while k - kl > 1:
                km = (kl + k) // 2
                if y < self.cdf[km]:
                    k = km
                else:
                    kl = km
        else:
            while True:
                u = 0.645 * self.doub()
                v = -0.63 + 1.25 * self.doub()
                v2 = v * v
                if v >= 0.0:
                    if v2 > 6.5 * u * (0.645 - u) * (u + 0.2):
                        continue
                elif v2 > 8.4 * u * (0.645 - u) * (u + 0.1):
                    continue
                k = math.floor(self.sq * (v / u) + self.np + 0.5)
                if k < 0 or k > self.n:
                    continue
                u2 = u * u
                if v >= 0.0:
                    if v2 < 12.25 * u2 * (0.615 - u) * (0.92 - u):
                        break
                elif v2 < 7.84 * u2 * (0.615 - u) * (1.2 - u):
                    break
                if self.n < 1024:
                    lf = self.logfact[k] + self.logfact[self.n - k]
                else:
                    lf = gammln(k + 1.0) + gammln(self.n - k + 1.0)
                b = self.sq * math.exp(self.glnp + k * self.plog + (self.n - k) * self.pclog - lf)
                if u2 < b:
                    break
        if self.p != self.pp:
            k = self.n - k
        return k


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    out = []
    if op == "EXP":
        d = Expondev(float(toks[1]), int(toks[2]))
        n = int(toks[3])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "LOGISTIC":
        d = Logisticdev(float(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "CAUCHY":
        d = Cauchydev(float(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "NORMAL":
        d = Normaldev(float(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "BOXMULLER":
        d = NormaldevBM(float(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "RAYLEIGH":
        r = Ran(int(toks[1]))
        n = int(toks[2])
        for _ in range(n):
            while True:
                x = r.doub()
                if x != 0.0:
                    break
            out.append("%.6f" % (canon(math.sqrt(-2.0 * math.log(x))) + 0.0))
    elif op == "GAMMA":
        d = Gammadev(float(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = ["%.6f" % (canon(d.dev()) + 0.0) for _ in range(n)]
    elif op == "CHISQ_DEV":
        d = Gammadev(0.5 * float(toks[1]), 1.0, int(toks[2]))
        n = int(toks[3])
        out = ["%.6f" % (canon(2.0 * d.dev()) + 0.0) for _ in range(n)]
    elif op == "STUDENTT_DEV":
        r = Ran(int(toks[4]))
        nu, mu, sig = float(toks[1]), float(toks[2]), float(toks[3])
        n = int(toks[5])
        for _ in range(n):
            while True:
                u1 = r.doub()
                if u1 != 0.0:
                    break
            u2 = r.doub()
            y = math.sqrt(math.pow(u1, -2.0 / nu) - 1.0) * math.cos(6.283185307179586 * u2)
            out.append("%.6f" % (canon(mu + sig * y) + 0.0))
    elif op == "BETA_DEV":
        dx = Gammadev(float(toks[1]), 1.0, int(toks[3]))
        dy = Gammadev(float(toks[2]), 1.0, int(toks[3]) + 1)
        n = int(toks[4])
        for _ in range(n):
            x, y = dx.dev(), dy.dev()
            out.append("%.6f" % (canon(x / (x + y)) + 0.0))
    elif op == "F_DEV":
        nu1, nu2 = float(toks[1]), float(toks[2])
        dx = Gammadev(0.5 * nu1, 1.0, int(toks[3]))
        dy = Gammadev(0.5 * nu2, 1.0, int(toks[3]) + 1)
        n = int(toks[4])
        for _ in range(n):
            x, y = dx.dev(), dy.dev()
            b = x / (x + y)
            out.append("%.6f" % (canon(nu2 * b / (nu1 * (1.0 - b))) + 0.0))
    elif op == "POISSON":
        d = Poissondev(float(toks[1]), int(toks[2]))
        n = int(toks[3])
        out = [str(d.dev()) for _ in range(n)]
    elif op == "BINOMIAL":
        d = Binomialdev(int(toks[1]), float(toks[2]), int(toks[3]))
        n = int(toks[4])
        out = [str(d.dev()) for _ in range(n)]
    else:
        return
    sys.stdout.write(" ".join(out) + "\n")


main()
