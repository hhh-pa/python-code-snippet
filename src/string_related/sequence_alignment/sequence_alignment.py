import sys

MATCH = 2
MISMATCH = -1
GAP = -2

def solve_global(s1, s2):
    n = len(s1)
    m = len(s2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + GAP
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + GAP

    for i in range(1, n + 1):
        dpi = dp[i]
        dpprev = dp[i - 1]
        c1 = s1[i - 1]
        for j in range(1, m + 1):
            diag = dpprev[j - 1] + (MATCH if c1 == s2[j - 1] else MISMATCH)
            up = dpprev[j] + GAP
            left = dpi[j - 1] + GAP
            dpi[j] = max(diag, up, left)

    a1 = []
    a2 = []
    i = n
    j = m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (MATCH if s1[i - 1] == s2[j - 1] else MISMATCH):
            a1.append(s1[i - 1])
            a2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP:
            a1.append(s1[i - 1])
            a2.append('-')
            i -= 1
        else:
            a1.append('-')
            a2.append(s2[j - 1])
            j -= 1

    a1.reverse()
    a2.reverse()
    print(dp[n][m])
    print("".join(a1))
    print("".join(a2))

def solve_local(s1, s2):
    n = len(s1)
    m = len(s2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_score = 0
    max_i = 0
    max_j = 0

    for i in range(1, n + 1):
        dpi = dp[i]
        dpprev = dp[i - 1]
        c1 = s1[i - 1]
        for j in range(1, m + 1):
            diag = dpprev[j - 1] + (MATCH if c1 == s2[j - 1] else MISMATCH)
            up = dpprev[j] + GAP
            left = dpi[j - 1] + GAP
            score = max(0, diag, up, left)
            dpi[j] = score
            if score > max_score:
                max_score = score
                max_i = i
                max_j = j

    a1 = []
    a2 = []
    i = max_i
    j = max_j
    while i > 0 and j > 0 and dp[i][j] > 0:
        if dp[i][j] == dp[i - 1][j - 1] + (MATCH if s1[i - 1] == s2[j - 1] else MISMATCH):
            a1.append(s1[i - 1])
            a2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + GAP:
            a1.append(s1[i - 1])
            a2.append('-')
            i -= 1
        else:
            a1.append('-')
            a2.append(s2[j - 1])
            j -= 1

    a1.reverse()
    a2.reverse()
    print(max_score)
    print("".join(a1))
    print("".join(a2))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    s1 = tokens[1]
    s2 = tokens[2]

    if mode == "GLOBAL":
        solve_global(s1, s2)
    else:
        solve_local(s1, s2)

if __name__ == "__main__":
    main()
