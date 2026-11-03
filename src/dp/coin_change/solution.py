import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    coins = [int(tokens[2 + i]) for i in range(m)]
    dp = [0] * (n + 1)
    dp[0] = 1
    for c in coins:
        for x in range(c, n + 1):
            dp[x] += dp[x - c]
    print(dp[n])

if __name__ == '__main__':
    main()
