# Band-diagonal linear solver (NR 2.4): Bandec LU with partial pivoting
# plus determinant, following the NR algorithm verbatim.
import sys


def fmt(v):
    w = 0.0 if abs(v) < 5e-7 else v
    return f"{w + 0.0:.6f}"


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    n, m1, m2 = int(toks[1]), int(toks[2]), int(toks[3])
    nums = [float(v) for v in toks[4:]]
    full = [nums[i * n:(i + 1) * n] for i in range(n)]
    b = nums[n * n:n * n + n]
    mm = m1 + m2 + 1
    au = [[0.0] * mm for _ in range(n)]
    for i in range(n):
        for k in range(max(0, i - m1), min(n, i + m2 + 1)):
            au[i][k - i + m1] = full[i][k]
    al = [[0.0] * max(m1, 1) for _ in range(n)]
    indx = [0] * n
    TINY = 1.0e-40
    l = m1
    for i in range(m1):
        for j in range(m1 - i, mm):
            au[i][j - l] = au[i][j]
        l -= 1
        for j in range(mm - l - 1, mm):
            au[i][j] = 0.0
    d = 1.0
    l = m1
    for k in range(n):
        dum = au[k][0]
        i = k
        if l < n:
            l += 1
        for j in range(k + 1, l):
            if abs(au[j][0]) > abs(dum):
                dum = au[j][0]
                i = j
        indx[k] = i + 1
        if dum == 0.0:
            au[k][0] = TINY
        if i != k:
            d = -d
            for j in range(mm):
                au[k][j], au[i][j] = au[i][j], au[k][j]
        for ii in range(k + 1, l):
            dum = au[ii][0] / au[k][0]
            al[k][ii - k - 1] = dum
            for j in range(1, mm):
                au[ii][j - 1] = au[ii][j] - dum * au[k][j]
            au[ii][mm - 1] = 0.0
    if op == "DET":
        dd = d
        for i in range(n):
            dd *= au[i][0]
        print(fmt(dd))
        return
    x = list(b)
    l = m1
    for k in range(n):
        j = indx[k] - 1
        if j != k:
            x[k], x[j] = x[j], x[k]
        if l < n:
            l += 1
        for j in range(k + 1, l):
            x[j] -= al[k][j - k - 1] * x[k]
    l = 1
    for i in range(n - 1, -1, -1):
        dum = x[i]
        for k in range(1, l):
            dum -= au[i][k] * x[k + i]
        x[i] = dum / au[i][0]
        if l < mm:
            l += 1
    print(" ".join(fmt(v) for v in x))


main()
