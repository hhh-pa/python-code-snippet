import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(tokens[idx])
        s = int(tokens[idx + 1])
        idx += 2
        w = [int(tokens[idx + i]) for i in range(n)]
        idx += n
        dp = [0] * (s + 1)
        for i in range(s + 1):
            cur = dp[i]
            for weight in w:
                if weight <= i:
                    val = dp[i - weight] + weight
                    if val > cur:
                        cur = val
            dp[i] = cur
        out.append(str(dp[s]))
    print("\n".join(out))

if __name__ == '__main__':
    main()
