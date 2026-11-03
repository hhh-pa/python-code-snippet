import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    p = [int(tokens[1 + i]) for i in range(n)]

    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        b = -2147483648
        for j in range(1, i + 1):
            if j <= n:
                val = p[j - 1] + dp[i - j]
                if val > b:
                    b = val
        dp[i] = 0 if b == -2147483648 else b

    print(dp[n])

if __name__ == '__main__':
    main()
