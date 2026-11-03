import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    k = int(tokens[0])
    n = int(tokens[1])
    if n <= 0:
        print(0)
        return
    if k <= 0:
        print(-1)
        return
    if k == 1:
        print(n)
        return
    dp = [0] * (k + 1)
    m = 0
    while dp[k] < n:
        m += 1
        for e in range(k, 0, -1):
            v = dp[e] + dp[e - 1] + 1
            dp[e] = n + 1 if v > n else v
    print(m)

if __name__ == '__main__':
    main()
