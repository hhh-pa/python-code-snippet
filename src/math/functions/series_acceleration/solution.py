# Series acceleration (NR 5.3): epsilon algorithm and Levin u-transform.
#
import sys

SMALL = 2.2250738585072014e-307
BIG = 1.7976931348623157e308


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    a = [float(v) for v in toks[2:2 + n]]
    val = 0.0
    if op == "EPSALG":
        e = [0.0] * n
        nn = 0
        s = 0.0
        for k in range(n):
            s += a[k]
            e[nn] = s
            temp2 = 0.0
            for j in range(nn, 0, -1):
                temp1 = temp2
                temp2 = e[j - 1]
                diff = e[j] - temp2
                if abs(diff) <= SMALL:
                    e[j - 1] = BIG
                else:
                    e[j - 1] = temp1 + 1.0 / diff
            nn += 1
            val = e[0] if nn & 1 else e[1]
    else:
        numer = [0.0] * n
        denom = [0.0] * n
        nn = 0
        s = 0.0
        lastval = 0.0
        for k in range(n):
            s += a[k]
            omega = (1.0 + nn) * a[k]
            term = 1.0 / (1.0 + nn)
            denom[nn] = term / omega
            numer[nn] = s * denom[nn]
            if nn > 0:
                ratio = (1.0 + nn - 1.0) * term
                for j in range(1, nn + 1):
                    fact = (nn - j + 1.0) * term
                    numer[nn - j] = numer[nn - j + 1] - fact * numer[nn - j]
                    denom[nn - j] = denom[nn - j + 1] - fact * denom[nn - j]
                    term = term * ratio
            nn += 1
            val = lastval if abs(denom[0]) < SMALL else numer[0] / denom[0]
            lastval = val
    w = 0.0 if abs(val) < 5e-7 else val
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
