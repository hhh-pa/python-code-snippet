import sys

def edist(a, b):
    n = len(a)
    m = len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        dpi = dp[i]
        dpprev = dp[i - 1]
        ai = a[i - 1]
        for j in range(1, m + 1):
            c = 0 if ai == b[j - 1] else 1
            dpi[j] = min(dpprev[j] + 1, dpi[j - 1] + 1, dpprev[j - 1] + c)
    return dp[n][m]

def align2(c, s):
    n = len(c)
    m = len(s)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        dpi = dp[i]
        dpprev = dp[i - 1]
        ci = c[i - 1]
        for j in range(1, m + 1):
            cc = 0 if ci == s[j - 1] else 1
            dpi[j] = min(dpprev[j] + 1, dpi[j - 1] + 1, dpprev[j - 1] + cc)

    rc = []
    rs = []
    i = n
    j = m
    while i > 0 or j > 0:
        cur = dp[i][j]
        if i > 0 and j > 0 and cur == dp[i - 1][j - 1] + (0 if c[i - 1] == s[j - 1] else 1):
            rc.append(c[i - 1])
            rs.append(s[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and cur == dp[i - 1][j] + 1:
            rc.append(c[i - 1])
            rs.append('-')
            i -= 1
        else:
            rc.append('-')
            rs.append(s[j - 1])
            j -= 1

    rc.reverse()
    rs.reverse()
    return "".join(rc), "".join(rs)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    strs = [next(it) for _ in range(n)]

    best = 0
    besttot = -1
    for c in range(n):
        tot = sum(edist(strs[c], strs[i]) for i in range(n))
        if besttot < 0 or tot < besttot:
            besttot = tot
            best = c

    rows = [strs[best]]
    rowpos = [-1] * n
    rowpos[best] = 0

    for idx in range(n):
        if idx == best:
            continue
        N, S = align2(strs[best], strs[idx])
        R = rows[0]
        num_rows = len(rows)
        nr = [[] for _ in range(num_rows + 1)]
        i = 0
        j = 0
        len_R = len(R)
        len_N = len(N)

        while i < len_R or j < len_N:
            if j < len_N and N[j] == '-':
                for r in range(num_rows):
                    nr[r].append('-')
                nr[num_rows].append(S[j])
                j += 1
            elif i < len_R and R[i] == '-':
                for r in range(num_rows):
                    nr[r].append(rows[r][i])
                nr[num_rows].append('-')
                i += 1
            else:
                for r in range(num_rows):
                    nr[r].append(rows[r][i])
                nr[num_rows].append(S[j])
                i += 1
                j += 1

        rows = ["".join(nr[r]) for r in range(num_rows + 1)]
        rowpos[idx] = len(rows) - 1

    L = len(rows[0])
    sp = 0
    num_r = len(rows)
    for c in range(L):
        col = [rows[r][c] for r in range(num_r)]
        for a in range(num_r):
            for b in range(a + 1, num_r):
                if col[a] != col[b]:
                    sp += 1

    print(sp)
    for i in range(n):
        print(rows[rowpos[i]])

if __name__ == "__main__":
    main()
