# Multivariate normal deviates (NR 7.4).
import math
import sys

M64 = 0xFFFFFFFFFFFFFFFF


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


def canon(v):
    return 0.0 if abs(v) < 5e-7 else v


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    p = 0
    mm = int(toks[p])
    p += 1
    mean = [float(toks[p + i]) for i in range(mm)]
    p += mm
    a = [[float(toks[p + i * mm + j]) for j in range(mm)] for i in range(mm)]
    p += mm * mm
    seed = int(toks[p])
    n = int(toks[p + 1])
    lmat = [[0.0] * mm for _ in range(mm)]
    for i in range(mm):
        for j in range(i + 1):
            s = a[i][j]
            for k in range(j):
                s -= lmat[i][k] * lmat[j][k]
            lmat[i][j] = math.sqrt(s) if i == j else s / lmat[j][j]
    r = Ran(seed)
    lines = []
    for _ in range(n):
        spt = []
        for _ in range(mm):
            while True:
                u = r.doub()
                v = 1.7156 * (r.doub() - 0.5)
                x = u - 0.449871
                y = abs(v) + 0.386595
                q = x * x + y * (0.19600 * y - 0.25472 * x)
                if not (q > 0.27597 and (q > 0.27846 or v * v > -4.0 * math.log(u) * u * u)):
                    spt.append(v / u)
                    break
        pt = []
        for i in range(mm):
            s = 0.0
            for j in range(i + 1):
                s += lmat[i][j] * spt[j]
            pt.append(s + mean[i])
        lines.append(" ".join("%.6f" % (canon(v) + 0.0) for v in pt))
    sys.stdout.write("\n".join(lines) + "\n")


main()
