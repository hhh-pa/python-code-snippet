# Linear feedback shift registers (NR 7.5).
import sys


def matmul_into(dst, x, y, nn):
    tmp = [0] * (nn * nn)
    for i in range(nn):
        for j in range(nn):
            s = 0
            for k in range(nn):
                s += x[i * nn + k] * y[k * nn + j]
            tmp[i * nn + j] = s & 1
    dst[:] = tmp


def primpolytest(n):
    nn = 32
    factors = (3, 5, 17, 257, 65537)
    t = [0] * (nn * nn)
    a = [0] * (nn * nn)
    p = [0] * (nn * nn)
    tnm1 = (1 << 32) - 1
    if n > (tnm1 >> 1):
        return 0
    for i in range(1, nn):
        t[i * nn + (i - 1)] = 1
    j = 0
    m = n
    while m:
        if m & 1:
            t[j] = 1
        m >>= 1
        j += 1
    t[nn - 1] = 1
    for rnd in range(6):
        pw = tnm1 if rnd == 0 else tnm1 // factors[rnd - 1]
        a[:] = t
        for k in range(nn * nn):
            p[k] = 0
        for k in range(nn):
            p[k * nn + k] = 1
        e = pw
        while True:
            if e & 1:
                matmul_into(p, p, a, nn)
            e >>= 1
            if e == 0:
                break
            matmul_into(a, a, a, nn)
        ident = 1
        for i in range(nn):
            for k in range(nn):
                if i == k:
                    if p[i * nn + k] != 1:
                        ident = 0
                elif p[i * nn + k] != 0:
                    ident = 0
        if rnd == 0:
            if ident != 1:
                return 0
        elif ident == 1:
            return 0
    return 1


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op == "STEP":
        maskp = int(toks[1]) & 0xFFFFFFFF
        maskn = int(toks[2]) & 0xFFFFFFFF
        a = int(toks[3]) & 0xFFFFFFFF
        n = int(toks[4])
        out = []
        for _ in range(n):
            if a & maskn:
                a = (((a ^ maskp) << 1) | 1) & 0xFFFFFFFF
            else:
                a = (a << 1) & 0xFFFFFFFF
            out.append(str(a))
        sys.stdout.write(" ".join(out) + "\n")
    elif op == "ISPRIMITIVE":
        sys.stdout.write("%d\n" % primpolytest(int(toks[1])))


main()
