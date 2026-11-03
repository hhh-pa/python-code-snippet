import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    idx = 1
    out = []
    for _ in range(t):
        s = int(tokens[idx])
        n = int(tokens[idx + 1])
        idx += 2
        dp = [0] * (s + 1)
        for _ in range(n):
            w = int(tokens[idx])
            v = int(tokens[idx + 1])
            idx += 2
            for j in range(s, w - 1, -1):
                if dp[j - w] + v > dp[j]:
                    dp[j] = dp[j - w] + v
        out.append(str(dp[s]))
    print("\n".join(out))

if __name__ == '__main__':
    main()
