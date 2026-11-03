import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    idx = 2
    a = [int(tokens[idx + i]) for i in range(n)]
    idx += n
    b = [int(tokens[idx + i]) for i in range(m)]
    idx += m
    
    # x = b, y = a
    x = b
    y = a
    lx = len(x)
    ly = len(y)
    dp = [[0] * (ly + 1) for _ in range(lx + 1)]
    for i in range(1, lx + 1):
        xi = x[i - 1]
        dpi = dp[i]
        dp_prev = dp[i - 1]
        for j in range(1, ly + 1):
            if xi == y[j - 1]:
                dpi[j] = dp_prev[j - 1] + 1
            elif dp_prev[j] > dpi[j - 1]:
                dpi[j] = dp_prev[j]
            else:
                dpi[j] = dpi[j - 1]
                
    i, j = lx, ly
    ans = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            ans.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    ans.reverse()
    print(*(ans))

if __name__ == '__main__':
    main()
