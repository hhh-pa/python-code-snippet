# Polynomial and derivatives at a point (NR 5.1, ddpoly).
#
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    m = int(toks[1])
    c = [float(v) for v in toks[2:3 + n]]
    x = float(toks[3 + n])
    pd = [0.0] * (m + 1)
    pd[0] = c[n]
    for i in range(n - 1, -1, -1):
        nnd = m if m < n - i else n - i
        for j in range(nnd, 0, -1):
            pd[j] = pd[j] * x + pd[j - 1]
        pd[0] = pd[0] * x + c[i]
    cnst = 1.0
    for i in range(2, m + 1):
        cnst *= i
        pd[i] *= cnst
    out = []
    for v in pd:
        w = 0.0 if abs(v) < 5e-7 else v
        out.append("%.6f" % (w + 0.0))
    sys.stdout.write(" ".join(out) + "\n")


main()
