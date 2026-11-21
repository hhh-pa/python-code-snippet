# Continued fraction evaluation (NR 5.2, modified Lentz's method).
# Port of the C++ reference.
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    b0 = float(toks[1])
    tiny = 1.0e-30
    f = b0 if b0 != 0.0 else tiny
    c = f
    d = 0.0
    for j in range(1, n + 1):
        a = float(toks[2 * j])
        b = float(toks[2 * j + 1])
        d = b + a * d
        if d == 0.0:
            d = tiny
        c = b + a / c
        if c == 0.0:
            c = tiny
        d = 1.0 / d
        f *= c * d
    w = 0.0 if abs(f) < 5e-7 else f
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
