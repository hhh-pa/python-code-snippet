import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    n = len(s)
    if n == 0:
        print(0)
        return

    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = (dp[i + 1][j - 1] if length > 2 else 0) + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    print(dp[0][n - 1])

if __name__ == '__main__':
    main()
