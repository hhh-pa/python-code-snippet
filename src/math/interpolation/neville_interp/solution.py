# Polynomial interpolation by Neville's algorithm (NR 3.2). Port of the C++ reference.
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
    xa = nums[:n]
    ya = nums[n:2 * n]
    q = int(nums[2 * n])
    qs = nums[2 * n + 1:2 * n + 1 + q]
    out = []
    for x in qs:
        c = list(ya)
        d = list(ya)
        dif = abs(x - xa[0])
        ns = 0
        for i in range(n):
            dift = abs(x - xa[i])
            if dift < dif:
                ns = i
                dif = dift
        y = ya[ns]
        ns -= 1
        dy = 0.0
        for m in range(1, n):
            for i in range(n - m):
                ho = xa[i] - x
                hp = xa[i + m] - x
                w = c[i + 1] - d[i]
                den = w / (ho - hp)
                d[i] = hp * den
                c[i] = ho * den
            if 2 * (ns + 1) < (n - m):
                dy = c[ns + 1]
            else:
                dy = d[ns]
                ns -= 1
            y += dy
        out.append(f"{fmt(y)} {fmt(dy)}")
    print("\n".join(out))


main()
