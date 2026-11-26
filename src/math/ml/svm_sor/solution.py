# Support vector machines: Mangasarian-Musicant 1-norm soft-margin
# variant solved by successive overrelaxation (SOR) with linear,
# polynomial, and Gaussian kernels.
# Reference: Press et al., Numerical Recipes 3e, Section 16.5
# (Svm/Svmgenkernel from svm.h, vendoring Ran from 7.1 and
# Indexx::index from 8.2).
# Documented decisions: nrelax is an explicit input (fixed group
# count, never data-dependent convergence); Ran(21) is reseeded
# per SVMTRAIN exactly as the book's Svm constructor; Indexx is
# the book's quicksort+insertion hybrid verbatim (its tie order
# feeds the update sequence); Svm::relax updates alph[j] with
# (om/(ker+1))*(y*sum-1) and projection MAX(0,MIN(lambda,.));
# y values are used as given (the book assumes +-1 without
# checking); m, n >= 1 and 1 <= nrelax <= 100000 enforced,
# m <= 2048 and n <= 4096 bound the kernel matrix (robustness
# caps; the book checks none of these); unknown kernels flag.
# No online-judge problem found -- fixtures are self-generated
# (KKT/formula oracle), no header link.
import math
import sys

MASK64 = 0xFFFFFFFFFFFFFFFF
MASK32 = 0xFFFFFFFF


def fmt6(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return "%.6f" % (w + 0.0)


class BadArgs(Exception):
    pass


class Ran:
    def __init__(self, j):
        self.v = 4101842887655102017
        self.w = 1
        self.u = (j ^ self.v) & MASK64
        self.int64()
        self.v = self.u
        self.int64()
        self.w = self.v
        self.int64()

    def int64(self):
        self.u = (self.u * 2862933555777941757 + 7046029254386353087) & MASK64
        self.v ^= self.v >> 17
        self.v ^= (self.v << 31) & MASK64
        self.v ^= self.v >> 8
        self.v &= MASK64
        self.w = (4294957665 * (self.w & MASK32) + (self.w >> 32)) & MASK64
        x = self.u ^ ((self.u << 21) & MASK64)
        x ^= x >> 35
        x ^= (x << 4) & MASK64
        x &= MASK64
        return ((x + self.v) & MASK64) ^ self.w

    def int32(self):
        return self.int64() & MASK32


def indexx(arr):
    m = 7
    nstack = 64
    n = len(arr)
    indx = list(range(n))
    istack = [0] * nstack
    ir = n - 1
    l = 0
    jstack = -1
    while True:
        if ir - l < m:
            for j in range(l + 1, ir + 1):
                indxt = indx[j]
                a = arr[indxt]
                i = j - 1
                while i >= l:
                    if arr[indx[i]] <= a:
                        break
                    indx[i + 1] = indx[i]
                    i -= 1
                indx[i + 1] = indxt
            if jstack < 0:
                break
            ir = istack[jstack]
            jstack -= 1
            l = istack[jstack]
            jstack -= 1
        else:
            k = (l + ir) >> 1
            indx[k], indx[l + 1] = indx[l + 1], indx[k]
            if arr[indx[l]] > arr[indx[ir]]:
                indx[l], indx[ir] = indx[ir], indx[l]
            if arr[indx[l + 1]] > arr[indx[ir]]:
                indx[l + 1], indx[ir] = indx[ir], indx[l + 1]
            if arr[indx[l]] > arr[indx[l + 1]]:
                indx[l], indx[l + 1] = indx[l + 1], indx[l]
            i = l + 1
            j = ir
            indxt = indx[l + 1]
            a = arr[indxt]
            while True:
                i += 1
                while arr[indx[i]] < a:
                    i += 1
                j -= 1
                while arr[indx[j]] > a:
                    j -= 1
                if j < i:
                    break
                indx[i], indx[j] = indx[j], indx[i]
            indx[l + 1] = indx[j]
            indx[j] = indxt
            jstack += 2
            if jstack >= nstack:
                raise BadArgs()
            if ir - i + 1 >= j - l:
                istack[jstack] = ir
                istack[jstack - 1] = i
                ir = j - 1
            else:
                istack[jstack] = j - 1
                istack[jstack - 1] = l
                l = i
    return indx


class Kernel:
    def __init__(self, kind, data, params):
        self.kind = kind
        self.data = data
        self.m = len(data)
        self.n = len(data[0])
        self.mu = [0.0] * self.n
        for i in range(self.m):
            for j in range(self.n):
                self.mu[j] += data[i][j]
        for j in range(self.n):
            self.mu[j] /= self.m
        self.pa, self.pb, self.pd, self.ps = params
        self.ker = [[0.0] * self.m for _ in range(self.m)]
        for i in range(self.m):
            for j in range(i + 1):
                v = self.call(self.data[i], self.data[j])
                self.ker[i][j] = v
                self.ker[j][i] = v

    def call(self, xi, xj):
        if self.kind == "LINEAR":
            dott = 0.0
            for k in range(self.n):
                dott += (xi[k] - self.mu[k]) * (xj[k] - self.mu[k])
            return dott
        if self.kind == "POLY":
            dott = 0.0
            for k in range(self.n):
                dott += xi[k] * xj[k]
            return math.pow(self.pa * dott + self.pb, self.pd)
        dott = 0.0
        for k in range(self.n):
            dott += (xi[k] - xj[k]) * (xi[k] - xj[k])
        return math.exp(-0.5 * dott / (self.ps * self.ps))

    def call_jx(self, j, x):
        return self.call(self.data[j], x)


class Svm:
    def __init__(self, gker, y):
        self.gker = gker
        self.y = y
        self.m = len(y)
        self.alph = [0.0] * self.m
        self.alphold = [0.0] * self.m
        self.ran = Ran(21)
        self.alphinit = False
        self.dalph = 0.0

    def relax(self, lam, om):
        m = self.m
        y = self.y
        ker = self.gker.ker
        alph = self.alph
        if not self.alphinit:
            for j in range(m):
                alph[j] = 0.0
            self.alphinit = True
        self.alphold = list(alph)
        x = indexx(alph)
        fnz = 0
        while fnz < m and alph[x[fnz]] == 0.0:
            fnz += 1
        # NOTE: the book breaks on != 0.0; == 0.0 loop is equivalent.
        j = fnz
        while j < m - 2:
            k = j + (self.ran.int32() % (m - j))
            x[j], x[k] = x[k], x[j]
            j += 1
        for jj in range(m):
            j = x[jj]
            s = 0.0
            for kk in range(fnz, m):
                k = x[kk]
                s += (ker[j][k] + 1.0) * y[k] * alph[k]
            alph[j] = alph[j] - (om / (ker[j][j] + 1.0)) * (y[j] * s - 1.0)
            alph[j] = max(0.0, min(lam, alph[j]))
            if jj < fnz and alph[j] != 0.0:
                fnz -= 1
                x[fnz], x[jj] = x[jj], x[fnz]
        yi = indexx(alph)
        fnz = 0
        while fnz < m and alph[yi[fnz]] == 0.0:
            fnz += 1
        fub = fnz
        while fub < m and alph[yi[fub]] != lam:
            fub += 1
        j = fnz
        while j < fub - 2:
            k = j + (self.ran.int32() % (fub - j))
            yi[j], yi[k] = yi[k], yi[j]
            j += 1
        pinsum = [0.0] * m
        for jj in range(fnz, fub):
            j = yi[jj]
            s = 0.0
            for kk in range(fub, m):
                k = yi[kk]
                s += (ker[j][k] + 1.0) * y[k] * alph[k]
            pinsum[jj] = s
        denom = float(fub - fnz + 1)
        niter = max(int(0.5 * (m + 1.0) * (m - fnz + 1.0) / (denom * denom)), 1)
        for _ in range(niter):
            for jj in range(fnz, fub):
                j = yi[jj]
                s = pinsum[jj]
                for kk in range(fnz, fub):
                    k = yi[kk]
                    s += (ker[j][k] + 1.0) * y[k] * alph[k]
                alph[j] = alph[j] - (om / (ker[j][j] + 1.0)) * (y[j] * s - 1.0)
                alph[j] = max(0.0, min(lam, alph[j]))
        dalph = 0.0
        for j in range(m):
            dalph += (alph[j] - self.alphold[j]) * (alph[j] - self.alphold[j])
        self.dalph = dalph
        return math.sqrt(dalph)

    def predict_k(self, kk):
        s = 0.0
        for j in range(self.m):
            s += self.alph[j] * self.y[j] * (self.gker.ker[j][kk] + 1.0)
        return s

    def predict_x(self, x):
        s = 0.0
        for j in range(self.m):
            s += self.alph[j] * self.y[j] * (self.gker.call_jx(j, x) + 1.0)
        return s


def emit(a, flag):
    print(" ".join([fmt6(v) for v in a] + [str(flag)]))


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op not in ("SVMTRAIN", "SVMPREDICT"):
        return
    ks = toks[1]
    pos = 2
    params = [0.0, 0.0, 0.0, 0.0]
    if ks == "LINEAR":
        kind = "LINEAR"
    elif ks == "POLY":
        kind = "POLY"
        params[0] = float(toks[pos])
        params[1] = float(toks[pos + 1])
        params[2] = float(toks[pos + 2])
        pos += 3
    elif ks == "GAUSS":
        kind = "GAUSS"
        params[3] = float(toks[pos])
        pos += 1
    else:
        kind = None
    if op == "SVMTRAIN":
        lam = float(toks[pos])
        om = float(toks[pos + 1])
        nrelax = int(toks[pos + 2])
        m = int(toks[pos + 3])
        n = int(toks[pos + 4])
        pos += 5
        shapeok = 1 <= m <= 2048 and 1 <= n <= 4096
        ok = shapeok and kind is not None and 1 <= nrelax <= 100000
        if not ok:
            emit([0.0] * ((2 * m + 1) if shapeok else 0), 1)
            return
        data = []
        for i in range(m):
            data.append([float(t) for t in toks[pos:pos + n]])
            pos += n
        y = [float(t) for t in toks[pos:pos + m]]
        try:
            kern = Kernel(kind, data, params)
            svm = Svm(kern, y)
            dalph = 0.0
            for _ in range(nrelax):
                dalph = svm.relax(lam, om)
            out = list(svm.alph) + [dalph]
            for i in range(m):
                out.append(svm.predict_k(i))
            emit(out, 0)
        except BadArgs:
            emit([0.0] * (2 * m + 1), 1)
    else:
        m = int(toks[pos])
        n = int(toks[pos + 1])
        pos += 2
        shapeok = 1 <= m <= 2048 and 1 <= n <= 4096
        ok = shapeok and kind is not None
        if not ok:
            emit([0.0] * (1 if shapeok else 0), 1)
            return
        data = []
        for i in range(m):
            data.append([float(t) for t in toks[pos:pos + n]])
            pos += n
        y = [float(t) for t in toks[pos:pos + m]]
        pos += m
        alph = [float(t) for t in toks[pos:pos + m]]
        pos += m
        x = [float(t) for t in toks[pos:pos + n]]
        kern = Kernel(kind, data, params)
        svm = Svm(kern, y)
        svm.alph = list(alph)
        svm.alphinit = True
        emit([svm.predict_x(x)], 0)


main()
