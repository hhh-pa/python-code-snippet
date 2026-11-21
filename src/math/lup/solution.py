"""LUP decomposition + solve with partial pivoting (CLRS 28)."""

import sys


def _decompose(a, perm):
    n = len(a)
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[piv][k] == 0.0:
            return False
        if piv != k:
            a[k], a[piv] = a[piv], a[k]
            perm[k], perm[piv] = perm[piv], perm[k]
        for i in range(k + 1, n):
            a[i][k] /= a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= a[i][k] * a[k][j]
    return True


def _solve(a, perm, b):
    n = len(a)
    y = [0.0] * n
    for i in range(n):
        s = b[perm[i]]
        for j in range(i):
            s -= a[i][j] * y[j]
        y[i] = s
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= a[i][j] * x[j]
        x[i] = s / a[i][i]
    return x


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    nums = list(map(float, data))
    n = int(nums[0])
    vals = nums[1:]
    a = [vals[i * n : (i + 1) * n] for i in range(n)]
    b = vals[n * n : n * n + n]
    perm = list(range(n))
    if not _decompose(a, perm):
        sys.stdout.write("SINGULAR")
        return
    x = _solve(a, perm, b)
    sys.stdout.write(" ".join("0.000000" if abs(v) < 5e-7 else f"{v:.6f}" for v in x))


if __name__ == "__main__":
    main()
