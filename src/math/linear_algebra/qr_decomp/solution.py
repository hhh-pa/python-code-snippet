# QR decomposition (NR 2.10, QRdcmp).
import math
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def sgn(a, b):
    return abs(a) if b >= 0.0 else -abs(a)


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n = int(toks[1])
    nums = [float(v) for v in toks[2:]]
    a = [nums[i * n:(i + 1) * n] for i in range(n)]
    rest = nums[n * n:]
    b = rest[:n]
    u = rest[:n] if op == "UPDATE" else [0.0] * n
    v = rest[n:2 * n] if op == "UPDATE" else [0.0] * n
    qt = [[0.0] * n for _ in range(n)]
    r = [row[:] for row in a]
    c = [0.0] * n
    d = [0.0] * n
    sing = False
    for k in range(n - 1):
        scale = 0.0
        for i in range(k, n):
            scale = max(scale, abs(r[i][k]))
        if scale == 0.0:
            sing = True
            c[k] = d[k] = 0.0
        else:
            for i in range(k, n):
                r[i][k] /= scale
            s = 0.0
            for i in range(k, n):
                s += r[i][k] * r[i][k]
            sigma = sgn(math.sqrt(s), r[k][k])
            r[k][k] += sigma
            c[k] = sigma * r[k][k]
            d[k] = -scale * sigma
            for j in range(k + 1, n):
                s = 0.0
                for i in range(k, n):
                    s += r[i][k] * r[i][j]
                tau = s / c[k]
                for i in range(k, n):
                    r[i][j] -= tau * r[i][k]
    d[n - 1] = r[n - 1][n - 1]
    if d[n - 1] == 0.0:
        sing = True
    for i in range(n):
        for j in range(n):
            qt[i][j] = 1.0 if i == j else 0.0
    for k in range(n - 1):
        if c[k] != 0.0:
            for j in range(n):
                s = 0.0
                for i in range(k, n):
                    s += r[i][k] * qt[i][j]
                s /= c[k]
                for i in range(k, n):
                    qt[i][j] -= s * r[i][k]
    for i in range(n):
        r[i][i] = d[i]
        for j in range(i):
            r[i][j] = 0.0

    def rotate(i, aa, bb):
        if aa == 0.0:
            cc, s = 0.0, 1.0 if bb >= 0.0 else -1.0
        elif abs(aa) > abs(bb):
            fact = bb / aa
            cc = sgn(1.0 / math.sqrt(1.0 + fact * fact), aa)
            s = fact * cc
        else:
            fact = aa / bb
            s = sgn(1.0 / math.sqrt(1.0 + fact * fact), bb)
            cc = fact * s
        for j in range(i, n):
            y, w = r[i][j], r[i + 1][j]
            r[i][j] = cc * y - s * w
            r[i + 1][j] = s * y + cc * w
        for j in range(n):
            y, w = qt[i][j], qt[i + 1][j]
            qt[i][j] = cc * y - s * w
            qt[i + 1][j] = s * y + cc * w

    if op == "UPDATE":
        w = list(u)
        k = n - 1
        while k >= 0 and w[k] == 0.0:
            k -= 1
        if k < 0:
            k = 0
        for i in range(k - 1, -1, -1):
            rotate(i, w[i], -w[i + 1])
            if w[i] == 0.0:
                w[i] = abs(w[i + 1])
            elif abs(w[i]) > abs(w[i + 1]):
                q = w[i + 1] / w[i]
                w[i] = abs(w[i]) * math.sqrt(1.0 + q * q)
            else:
                q = w[i] / w[i + 1]
                w[i] = abs(w[i + 1]) * math.sqrt(1.0 + q * q)
        for i in range(n):
            r[0][i] += w[0] * v[i]
        for i in range(k):
            rotate(i, r[i][i], -r[i + 1][i])
        for i in range(n):
            if r[i][i] == 0.0:
                sing = True
    if op in ("FACTOR", "UPDATE"):
        print("QT")
        for i in range(n):
            print(" ".join(fmt(v) for v in qt[i]))
        print("R")
        for i in range(n):
            print(" ".join(fmt(v) for v in r[i]))
        print(f"SINGULAR {1 if sing else 0}")
        return
    if sing:
        print("SINGULAR")
        return
    x = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += qt[i][j] * b[j]
        x[i] = s
    for i in range(n - 1, -1, -1):
        s = x[i]
        for j in range(i + 1, n):
            s -= r[i][j] * x[j]
        x[i] = s / r[i][i]
    print(" ".join(fmt(v) for v in x))


main()
