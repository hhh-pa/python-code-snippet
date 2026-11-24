# Uniform random generators (NR 7.1).
import sys

M64 = 0xFFFFFFFFFFFFFFFF
M32 = 0xFFFFFFFF


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
        self.w = (4294957665 * (self.w & M32) + (self.w >> 32)) & M64
        x = self.u ^ ((self.u << 21) & M64)
        x ^= x >> 35
        x ^= (x << 4) & M64
        return ((x + self.v) & M64) ^ self.w

    def doub(self):
        return 5.42101086242752217e-20 * float(self.int64())

    def int32(self):
        return self.int64() & M32


class Ranq1:
    def __init__(self, j):
        self.v = 4101842887655102017
        self.v ^= j
        self.v = self.int64()

    def int64(self):
        self.v ^= self.v >> 21
        self.v ^= (self.v << 35) & M64
        self.v ^= self.v >> 4
        return (self.v * 2685821657736338717) & M64

    def doub(self):
        return 5.42101086242752217e-20 * float(self.int64())


class Ranq2:
    def __init__(self, j):
        self.v = 4101842887655102017
        self.w = 1
        self.v ^= j
        self.w = self.int64()
        self.v = self.int64()

    def int64(self):
        self.v ^= self.v >> 17
        self.v ^= (self.v << 31) & M64
        self.v ^= self.v >> 8
        self.w = (4294957665 * (self.w & M32) + (self.w >> 32)) & M64
        return self.v ^ self.w

    def doub(self):
        return 5.42101086242752217e-20 * float(self.int64())


def ranhash64(u):
    v = (u * 3935559000370003845 + 2691343689449507681) & M64
    v ^= v >> 21
    v ^= (v << 37) & M64
    v ^= v >> 4
    v = (v * 4768777513237032717) & M64
    v ^= (v << 20) & M64
    v ^= v >> 41
    v ^= (v << 5) & M64
    return v


class Ranfib:
    def __init__(self, j):
        self.dtab = [0.0] * 55
        self.inext = 0
        self.inextp = 31
        init = Ranq1(j)
        for k in range(55):
            self.dtab[k] = init.doub()

    def doub(self):
        self.inext += 1
        if self.inext == 55:
            self.inext = 0
        self.inextp += 1
        if self.inextp == 55:
            self.inextp = 0
        dd = self.dtab[self.inext] - self.dtab[self.inextp]
        if dd < 0:
            dd += 1.0
        self.dtab[self.inext] = dd
        return dd

    def int32(self):
        return int(self.doub() * 4294967295.0)


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    out = []
    if op == "RAN":
        r = Ran(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append(str(r.int64()))
    elif op == "RAN_D":
        r = Ran(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append("%.6f" % (canon(r.doub()) + 0.0))
    elif op == "RAN32":
        r = Ran(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append(str(r.int32()))
    elif op == "RAN8":
        r = Ran(int(toks[1]))
        breg = 0
        bc = 0
        for _ in range(int(toks[2])):
            if bc != 0:
                bc -= 1
                breg >>= 8
                out.append(str(breg & 0xFF))
            else:
                bc -= 1
                breg = r.int64()
                bc = 7
                out.append(str(breg & 0xFF))
    elif op == "RANQ1":
        r = Ranq1(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append(str(r.int64()))
    elif op == "RANQ1_D":
        r = Ranq1(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append("%.6f" % (canon(r.doub()) + 0.0))
    elif op == "RANQ2":
        r = Ranq2(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append(str(r.int64()))
    elif op == "RANQ2_D":
        r = Ranq2(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append("%.6f" % (canon(r.doub()) + 0.0))
    elif op == "HASH64":
        out.append(str(ranhash64(int(toks[1]))))
    elif op == "HASH32":
        out.append(str(ranhash64(int(toks[1])) & M32))
    elif op == "HASH_D":
        out.append("%.6f" % (canon(5.42101086242752217e-20 * float(ranhash64(int(toks[1])))) + 0.0))
    elif op == "RANFIB_D":
        r = Ranfib(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append("%.6f" % (canon(r.doub()) + 0.0))
    elif op == "RANFIB_32":
        r = Ranfib(int(toks[1]))
        for _ in range(int(toks[2])):
            out.append(str(r.int32()))
    else:
        return
    sys.stdout.write(" ".join(out) + "\n")


main()
