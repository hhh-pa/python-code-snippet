# Generalized Fermi-Dirac integral (NR 6.10).
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 3:
        return
    kk = float(toks[0])
    etaa = float(toks[1])
    thetaa = float(toks[2])

    def f_trap(t):
        e = math.exp(-t)
        x = math.exp(t - e)
        return x * (1.0 + e) * math.pow(x, kk) * math.sqrt(1.0 + thetaa * 0.5 * x) \
            / (math.exp(x - etaa) + 1.0)

    def f_de(x, dl):
        pw = math.pow(dl, kk) if x < 1.0 else math.pow(x, kk)
        return pw * math.sqrt(1.0 + thetaa * 0.5 * x) / (math.exp(x - etaa) + 1.0)

    eps = 3.0e-9
    nmax = 11
    sm = 0.0
    olds = 0.0
    flag = 1
    if etaa <= 15.0:
        a = -4.5
        b = 5.0
        n = 0
        st = 0.0
        for i in range(1, nmax + 1):
            n += 1
            if n == 1:
                st = 0.5 * (b - a) * (f_trap(a) + f_trap(b))
            else:
                it = 1
                for _ in range(1, n - 1):
                    it <<= 1
                tnm = float(it)
                dl = (b - a) / tnm
                x = a + 0.5 * dl
                acc = 0.0
                for _ in range(it):
                    acc += f_trap(x)
                    x += dl
                st = 0.5 * (st + (b - a) * acc / tnm)
            sm = st
            if i > 3 and abs(sm - olds) <= eps * abs(olds):
                flag = 0
                break
            olds = sm
    else:
        hmax = 4.3
        aa = [0.0, etaa]
        bb = [etaa, etaa + 60.0]
        st = [0.0, 0.0]
        nn = [0, 0]
        for i in range(1, nmax + 1):
            sm = 0.0
            for r in range(2):
                nn[r] += 1
                if nn[r] == 1:
                    st[r] = hmax * 2.0 * (bb[r] - aa[r]) * 0.25 * \
                        f_de(0.5 * (bb[r] + aa[r]), 0.5 * (bb[r] - aa[r]))
                else:
                    it = 1
                    for _ in range(1, nn[r] - 1):
                        it <<= 1
                    twoh = hmax / it
                    t = 0.5 * twoh
                    acc = 0.0
                    for _ in range(it):
                        q = math.exp(-2.0 * math.sinh(t))
                        dl = (bb[r] - aa[r]) * q / (1.0 + q)
                        fact = q / ((1.0 + q) * (1.0 + q)) * math.cosh(t)
                        acc += fact * (f_de(aa[r] + dl, dl) + f_de(bb[r] - dl, dl))
                        t += twoh
                    st[r] = 0.5 * st[r] + (bb[r] - aa[r]) * twoh * acc
                sm += st[r]
            if i > 3 and abs(sm - olds) <= eps * abs(olds):
                flag = 0
                break
            olds = sm
    w = 0.0 if abs(sm) < 5e-7 else sm
    sys.stdout.write("%.6f %d\n" % (w + 0.0, flag))


main()
