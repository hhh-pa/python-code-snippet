# Vandermonde solve in O(n^2) (NR 2.8.1, vander).
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n = int(toks[0])
    nums = [float(v) for v in toks[1:]]
    x = nums[:n]
    q = nums[n:2 * n]
    w = [0.0] * n
    if n == 1:
        w[0] = q[0]
    else:
        c = [0.0] * n
        c[n - 1] = -x[0]
        for i in range(1, n):
            xx = -x[i]
            for j in range(n - 1 - i, n - 1):
                c[j] += xx * c[j + 1]
            c[n - 1] += xx
        for i in range(n):
            xx = x[i]
            t = b = 1.0
            s = q[n - 1]
            for k in range(n - 1, 0, -1):
                b = c[k] + xx * b
                s += q[k - 1] * b
                t = xx * t + b
            w[i] = s / t
    print(" ".join(fmt(v) for v in w))


main()
