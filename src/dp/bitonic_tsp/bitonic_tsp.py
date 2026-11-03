import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    x = [0.0] * n
    y = [0.0] * n
    idx = 1
    for i in range(n):
        x[i] = float(tokens[idx])
        y[i] = float(tokens[idx + 1])
        idx += 2
    if n <= 1:
        print(f"{0.0:.6f}")
        return
    if n == 2:
        d = math.hypot(x[1] - x[0], y[1] - y[0])
        print(f"{2 * d:.6f}")
        return

    def dist(a, b):
        return math.hypot(x[a] - x[b], y[a] - y[b])

    dp = [[1e100] * n for _ in range(n)]
    dp[0][1] = dist(0, 1)
    for j in range(2, n):
        for i in range(j - 1):
            dp[i][j] = dp[i][j - 1] + dist(j - 1, j)
        best = 1e100
        for k in range(j - 1):
            val = dp[k][j - 1] + dist(k, j)
            if val < best:
                best = val
        dp[j - 1][j] = best

    ans = dp[n - 2][n - 1] + dist(n - 2, n - 1)
    print(f"{ans:.6f}")

if __name__ == "__main__":
    main()
