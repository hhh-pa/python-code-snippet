import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    h = int(tokens[0])
    w = int(tokens[1])
    idx = 2
    e = []
    for _ in range(h):
        e.append([int(x) for x in tokens[idx : idx + w]])
        idx += w

    INF = 4 * 10**18
    dp = [[INF] * w for _ in range(h)]
    par = [[0] * w for _ in range(h)]

    for c in range(w):
        dp[0][c] = e[0][c]

    for r in range(1, h):
        dp_prev = dp[r - 1]
        dp_curr = dp[r]
        par_curr = par[r]
        er = e[r]
        for c in range(w):
            best = INF
            bi = c
            # pc in c-1, c, c+1
            start = max(0, c - 1)
            end = min(w - 1, c + 1)
            for pc in range(start, end + 1):
                if dp_prev[pc] < best:
                    best = dp_prev[pc]
                    bi = pc
            dp_curr[c] = er[c] + best
            par_curr[c] = bi

    mc = 0
    dp_last = dp[h - 1]
    for c in range(1, w):
        if dp_last[c] < dp_last[mc]:
            mc = c

    seam = [0] * h
    seam[h - 1] = mc
    for r in range(h - 1, 0, -1):
        seam[r - 1] = par[r][seam[r]]

    print(dp_last[mc])
    print(*(seam))

if __name__ == '__main__':
    main()
