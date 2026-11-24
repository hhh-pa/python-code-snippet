# Cubic spline interpolation (NR 3.3).
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    nums = [float(v) for v in toks[2:]]
    xv = nums[:n]
    yv = nums[n:2 * n]
    yp1, ypn = nums[2 * n], nums[2 * n + 1]
    y2 = [0.0] * n
    u = [0.0] * (n - 1)
    if yp1 > 0.99e99:
        y2[0] = u[0] = 0.0
    else:
        y2[0] = -0.5
        u[0] = (3.0 / (xv[1] - xv[0])) * ((yv[1] - yv[0]) / (xv[1] - xv[0]) - yp1)
    for i in range(1, n - 1):
        sig = (xv[i] - xv[i - 1]) / (xv[i + 1] - xv[i - 1])
        p = sig * y2[i - 1] + 2.0
        y2[i] = (sig - 1.0) / p
        ui = (yv[i + 1] - yv[i]) / (xv[i + 1] - xv[i]) - (yv[i] - yv[i - 1]) / (xv[i] - xv[i - 1])
        u[i] = (6.0 * ui / (xv[i + 1] - xv[i - 1]) - sig * u[i - 1]) / p
    if ypn > 0.99e99:
        qn = un = 0.0
    else:
        qn = 0.5
        un = (3.0 / (xv[n - 1] - xv[n - 2])) * (ypn - (yv[n - 1] - yv[n - 2]) / (xv[n - 1] - xv[n - 2]))
    y2[n - 1] = (un - qn * u[n - 2]) / (qn * y2[n - 2] + 1.0)
    for k in range(n - 2, -1, -1):
        y2[k] = y2[k] * y2[k + 1] + u[k]
    if op == "SECOND":
        print(" ".join(fmt(v) for v in y2))
        return
    q = int(nums[2 * n + 2])
    qs = nums[2 * n + 3:2 * n + 3 + q]
    out = []
    for x in qs:
        klo, khi = 0, n - 1
        while khi - klo > 1:
            k = (khi + klo) >> 1
            if xv[k] > x:
                khi = k
            else:
                klo = k
        jl = min(klo, n - 2)
        klo2, khi2 = jl, jl + 1
        h = xv[khi2] - xv[klo2]
        a = (xv[khi2] - x) / h
        b = (x - xv[klo2]) / h
        y = a * yv[klo2] + b * yv[khi2] + ((a * a * a - a) * y2[klo2] + (b * b * b - b) * y2[khi2]) * (h * h) / 6.0
        out.append(fmt(y))
    print("\n".join(out))


main()
