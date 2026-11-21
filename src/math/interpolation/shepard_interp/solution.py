# Shepard interpolation (NR 3.7.4). Port of the C++ reference.
import math
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    p = int(toks[0])
    n, dim = int(toks[1]), int(toks[2])
    nums = [float(v) for v in toks[3:]]
    pts = [nums[i * dim:(i + 1) * dim] for i in range(n)]
    vals = nums[n * dim:n * dim + n]
    q = int(nums[n * dim + n])
    qs = [nums[n * dim + n + 1 + i * dim:n * dim + n + 1 + (i + 1) * dim] for i in range(q)]
    out = []
    for pt in qs:
        num = den = 0.0
        exact = -1
        for i in range(n):
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(pt, pts[i])))
            if r == 0.0:
                exact = i
                break
            rp = 1.0
            for _ in range(p):
                rp *= r
            w = 1.0 / rp
            num += w * vals[i]
            den += w
        out.append(fmt(vals[exact]) if exact >= 0 else fmt(num / den))
    print("\n".join(out))


main()
