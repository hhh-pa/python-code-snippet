# Inverse of y = x log(x), smaller root (NR 6.11).
import math
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    y = float(toks[0])
    ooe = 0.367879441171442322
    if not (y > -ooe and y < 0.0):
        sys.stdout.write("0.000000\n")
        return
    to = 0.0
    if y < -0.2:
        u = math.log(ooe - math.sqrt(2.0 * ooe * (y + ooe)))
    else:
        u = -10.0
    while True:
        t = (math.log(y / u) - u) * (u / (1.0 + u))
        u += t
        if t < 1.0e-8 and abs(t + to) < 0.01 * abs(t):
            break
        to = t
        if not abs(t / u) > 1.0e-15:
            break
    ans = math.exp(u)
    w = 0.0 if abs(ans) < 5e-7 else ans
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
