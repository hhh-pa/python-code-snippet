import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "S2":
        n = int(tokens[1])
        k = int(tokens[2])
        dp = [0] * (k + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            ndp = [0] * (k + 1)
            for j in range(1, min(i, k) + 1):
                ndp[j] = j * dp[j] + dp[j-1]
            dp = ndp
        sys.stdout.write(str(dp[k]) + "\n")
    elif mode == "S1":
        n = int(tokens[1])
        k = int(tokens[2])
        dp = [0] * (k + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            ndp = [0] * (k + 1)
            for j in range(1, min(i, k) + 1):
                ndp[j] = -(i - 1) * dp[j] + dp[j-1]
            dp = ndp
        sys.stdout.write(str(dp[k]) + "\n")
    else:
        n = int(tokens[1])
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            ndp = [0] * (n + 1)
            for j in range(1, i + 1):
                ndp[j] = j * dp[j] + dp[j-1]
            dp = ndp
        sys.stdout.write(str(sum(dp)) + "\n")

if __name__ == "__main__":
    main()
