import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    A = tokens[0]
    B = tokens[1]
    n = len(A)
    m = len(B)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    memo = {}

    def solve_block(a0, a1, b0, b1, t0, t1, l0, l1):
        k = (a0, a1, b0, b1, t0, t1, l0, l1)
        if k in memo:
            return memo[k]
        T0 = 0
        T1 = t0
        T2 = t0 + t1
        L0 = 0
        L1 = l0
        L2 = l0 + l1
        x11 = min(T1 + 1, L1 + 1, L0 + (0 if a0 == b0 else 1))
        x12 = min(T2 + 1, x11 + 1, T1 + (0 if a0 == b1 else 1))
        x21 = min(x11 + 1, L2 + 1, L1 + (0 if a1 == b0 else 1))
        x22 = min(x12 + 1, x21 + 1, x11 + (0 if a1 == b1 else 1))
        v = (x21 - L2, x22 - x21, x12 - T2, x22 - x12)
        memo[k] = v
        return v

    def cell(i, j):
        c = 0 if A[i - 1] == B[j - 1] else 1
        return min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + c)

    nb = n // 2
    mb = m // 2

    for bi in range(nb):
        for bj in range(mb):
            i0 = 2 * bi
            j0 = 2 * bj
            t0 = dp[i0][j0 + 1] - dp[i0][j0]
            t1 = dp[i0][j0 + 2] - dp[i0][j0 + 1]
            l0 = dp[i0 + 1][j0] - dp[i0][j0]
            l1 = dp[i0 + 2][j0] - dp[i0 + 1][j0]
            v = solve_block(A[i0], A[i0 + 1], B[j0], B[j0 + 1], t0, t1, l0, l1)
            dp[i0 + 2][j0 + 1] = dp[i0 + 2][j0] + v[0]
            dp[i0 + 2][j0 + 2] = dp[i0 + 2][j0 + 1] + v[1]
            dp[i0 + 1][j0 + 2] = dp[i0][j0 + 2] + v[2]

    nodd = (n % 2 == 1)
    modd = (m % 2 == 1)
    if nodd and modd:
        for j in range(1, m):
            dp[n][j] = cell(n, j)
        for i in range(1, n + 1):
            dp[i][m] = cell(i, m)
    else:
        if modd:
            for i in range(1, n + 1):
                dp[i][m] = cell(i, m)
        if nodd:
            for j in range(1, m + 1):
                dp[n][j] = cell(n, j)

    print(dp[n][m])

if __name__ == "__main__":
    main()
