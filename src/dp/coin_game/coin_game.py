import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    v = [int(tokens[1 + i]) for i in range(n)]
    if n == 0:
        print(0)
        return
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = v[i]
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            a = dp[i + 2][j] if i + 2 <= j else 0
            b = dp[i + 1][j - 1] if i + 1 <= j - 1 else 0
            c = dp[i][j - 2] if i <= j - 2 else 0
            dp[i][j] = max(v[i] + min(a, b), v[j] + min(b, c))
    print(dp[0][n - 1])

if __name__ == '__main__':
    main()
