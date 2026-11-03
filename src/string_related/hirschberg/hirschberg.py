import sys

sys.setrecursionlimit(200000)

MATCH = 2
MISMATCH = -1
GAP = -2

def nw_score(x, y):
    m = len(y)
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for j in range(1, m + 1):
        prev[j] = prev[j - 1] + GAP

    for i in range(1, len(x) + 1):
        curr[0] = prev[0] + GAP
        xi = x[i - 1]
        for j in range(1, m + 1):
            diag = prev[j - 1] + (MATCH if xi == y[j - 1] else MISMATCH)
            up = prev[j] + GAP
            left = curr[j - 1] + GAP
            curr[j] = max(diag, up, left)
        prev = curr[:]
    return prev

def hirschberg(x, y):
    if not x:
        return '-' * len(y), y
    if not y:
        return x, '-' * len(x)

    if len(x) == 1 or len(y) == 1:
        n = len(x)
        m = len(y)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            dp[i][0] = dp[i - 1][0] + GAP
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j - 1] + GAP
        for i in range(1, n + 1):
            xi = x[i - 1]
            for j in range(1, m + 1):
                diag = dp[i - 1][j - 1] + (MATCH if xi == y[j - 1] else MISMATCH)
                up = dp[i - 1][j] + GAP
                left = dp[i][j - 1] + GAP
                dp[i][j] = max(diag, up, left)
        a1 = []
        a2 = []
        i = n
        j = m
        while i > 0 or j > 0:
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (MATCH if x[i - 1] == y[j - 1] else MISMATCH):
                a1.append(x[i - 1])
                a2.append(y[j - 1])
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP:
                a1.append(x[i - 1])
                a2.append('-')
                i -= 1
            else:
                a1.append('-')
                a2.append(y[j - 1])
                j -= 1
        a1.reverse()
        a2.reverse()
        return "".join(a1), "".join(a2)

    xlen = len(x)
    xmid = xlen // 2

    x_left = x[:xmid]
    x_right = x[xmid:]

    score_l = nw_score(x_left, y)
    score_r = nw_score(x_right[::-1], y[::-1])

    m = len(y)
    best_score = -10**9
    best_j = 0

    for j in range(m + 1):
        total = score_l[j] + score_r[m - j]
        if total > best_score:
            best_score = total
            best_j = j

    left_a1, left_a2 = hirschberg(x_left, y[:best_j])
    right_a1, right_a2 = hirschberg(x_right, y[best_j:])

    return left_a1 + right_a1, left_a2 + right_a2

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s1 = tokens[0]
    s2 = tokens[1]

    a1, a2 = hirschberg(s1, s2)
    score = 0
    for c1, c2 in zip(a1, a2):
        if c1 == '-' or c2 == '-':
            score += GAP
        elif c1 == c2:
            score += MATCH
        else:
            score += MISMATCH

    print(score)
    print(a1)
    print(a2)

if __name__ == "__main__":
    main()
