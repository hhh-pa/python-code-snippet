import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 1:
        print(0)
        return
    d = []
    idx = 1
    for i in range(n):
        row = [int(tokens[idx + j]) for j in range(n)]
        idx += n
        d.append(row)
        
    INF = 4 * 10**18
    N = 1 << n
    dp = [[INF] * n for _ in range(N)]
    dp[1][0] = 0
    
    for mask in range(N):
        if not (mask & 1):
            continue
        for u in range(n):
            if not (mask & (1 << u)) or dp[mask][u] == INF:
                continue
            cur = dp[mask][u]
            for v in range(1, n):
                if mask & (1 << v):
                    continue
                nm = mask | (1 << v)
                val = cur + d[u][v]
                if val < dp[nm][v]:
                    dp[nm][v] = val
                    
    full = N - 1
    ans = min(dp[full][u] + d[u][0] for u in range(n))
    print(ans)

if __name__ == '__main__':
    main()
