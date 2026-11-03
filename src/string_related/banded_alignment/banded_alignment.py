import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s1 = tokens[0]
    s2 = tokens[1]
    k = int(tokens[2])

    n = len(s1)
    m = len(s2)
    INF = 10**9

    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n + 1):
        low_j = max(0, i - k)
        high_j = min(m, i + k)
        dp_i = dp[i]
        dp_prev = dp[i - 1] if i > 0 else None
        s1_char = s1[i - 1] if i > 0 else ''

        for j in range(low_j, high_j + 1):
            if i == 0 and j == 0:
                continue
            best = INF
            if i > 0 and abs((i - 1) - j) <= k:
                val = dp_prev[j] + 1
                if val < best:
                    best = val
            if j > 0 and abs(i - (j - 1)) <= k:
                val = dp_i[j - 1] + 1
                if val < best:
                    best = val
            if i > 0 and j > 0 and abs((i - 1) - (j - 1)) <= k:
                cost = 0 if s1_char == s2[j - 1] else 1
                val = dp_prev[j - 1] + cost
                if val < best:
                    best = val
            if best < INF:
                dp_i[j] = best

    ans = dp[n][m]
    print(-1 if ans >= INF else ans)

if __name__ == "__main__":
    main()
