# Toeplitz solve in O(n^2) (NR 2.8.2, toeplz).
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
    r = nums[:2 * n - 1]
    y = nums[2 * n - 1:3 * n - 1]
    x = [0.0] * n
    n1 = n - 1
    x[0] = y[0] / r[n1]
    if n1 != 0:
        g = [0.0] * n1
        h = [0.0] * n1
        g[0] = r[n1 - 1] / r[n1]
        h[0] = r[n1 + 1] / r[n1]
        for m in range(n):
            m1 = m + 1
            sxn = -y[m1]
            sd = -r[n1]
            for j in range(m + 1):
                sxn += r[n1 + m1 - j] * x[j]
                sd += r[n1 + m1 - j] * g[m - j]
            x[m1] = sxn / sd
            for j in range(m + 1):
                x[j] -= x[m1] * g[m - j]
            if m1 == n1:
                break
            sgn = -r[n1 - m1 - 1]
            shn = -r[n1 + m1 + 1]
            sgd = -r[n1]
            for j in range(m + 1):
                sgn += r[n1 + j - m1] * g[j]
                shn += r[n1 + m1 - j] * h[j]
                sgd += r[n1 + j - m1] * h[m - j]
            g[m1] = sgn / sgd
            h[m1] = shn / sd
            k = m
            m2 = (m + 2) >> 1
            pp, qq = g[m1], h[m1]
            for j in range(m2):
                pt1, pt2 = g[j], g[k]
                qt1, qt2 = h[j], h[k]
                g[j] = pt1 - pp * qt2
                g[k] = pt2 - pp * qt1
                h[j] = qt1 - qq * pt2
                h[k] = qt2 - qq * pt1
                k -= 1
    print(" ".join(fmt(v) for v in x))


main()
