# Clenshaw's recurrence (NR 5.4). Port of the C++ reference.
import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    f0 = float(toks[1])
    f1 = float(toks[2])
    c = [float(v) for v in toks[3:4 + n]]
    base = 4 + n
    al = [0.0] + [float(v) for v in toks[base:base + n]]
    be = [0.0] + [float(v) for v in toks[base + n:base + 2 * n + 1]]
    y = [0.0] * (n + 3)
    for k in range(n, 0, -1):
        y[k] = al[k] * y[k + 1] + be[k + 1] * y[k + 2] + c[k]
    f = be[1] * f0 * y[2] + f1 * y[1] + f0 * c[0]
    w = 0.0 if abs(f) < 5e-7 else f
    sys.stdout.write("%.6f\n" % (w + 0.0))


main()
