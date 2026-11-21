# Rational interpolation (NR 3.4). Port of the C++ reference.
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
    xa = nums[:n]
    ya = nums[n:2 * n]
    rest = nums[2 * n:]
    out = []
    if op == "RATINT":
        TINY = 1.0e-99
        q = int(rest[0])
        qs = rest[1:1 + q]
        for x in qs:
            c = list(ya)
            d = [v + TINY for v in ya]
            hh = abs(x - xa[0])
            ns, exact = 0, -1
            for i in range(n):
                h = abs(x - xa[i])
                if h == 0.0:
                    exact = i
                if h < hh and exact < 0:
                    ns, hh = i, h
            if exact >= 0:
                out.append(f"{fmt(ya[exact])} {fmt(0.0)}")
                continue
            y = ya[ns]
            ns -= 1
            dy = 0.0
            for m in range(1, n):
                for i in range(n - m):
                    w = c[i + 1] - d[i]
                    h = xa[i + m] - x
                    t = (xa[i] - x) * d[i] / h
                    dd = t - c[i + 1]
                    dd = w / dd
                    d[i] = c[i + 1] * dd
                    c[i] = t * dd
                if 2 * (ns + 1) < (n - m):
                    dy = c[ns + 1]
                else:
                    dy = d[ns]
                    ns -= 1
                y += dy
            out.append(f"{fmt(y)} {fmt(dy)}")
        print("\n".join(out))
        return
    ddord = int(rest[0])
    q = int(rest[1])
    qs = rest[2:2 + q]
    w = [0.0] * n
    for k in range(n):
        imin = max(k - ddord, 0)
        imax = n - ddord - 1 if k >= n - ddord else k
        temp = -1.0 if (imin & 1) else 1.0
        s = 0.0
        for i in range(imin, imax + 1):
            jmax = min(i + ddord, n - 1)
            term = 1.0
            for j in range(i, jmax + 1):
                if j == k:
                    continue
                term *= xa[k] - xa[j]
            term = temp / term
            temp = -temp
            s += term
        w[k] = s
    for x in qs:
        num = den = 0.0
        exact = -1
        for i in range(n):
            h = x - xa[i]
            if h == 0.0:
                exact = i
                break
            t = w[i] / h
            num += t * ya[i]
            den += t
        out.append(fmt(ya[exact]) if exact >= 0 else fmt(num / den))
    print("\n".join(out))


main()
