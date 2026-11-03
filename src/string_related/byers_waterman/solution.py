import sys

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    A = tokens[0]
    B = tokens[1]
    D = int(tokens[2])

    n = len(A)
    m = len(B)

    F = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        F[i][0] = i
    for j in range(m + 1):
        F[0][j] = j

    for i in range(1, n + 1):
        Fi = F[i]
        Fprev = F[i - 1]
        Ai = A[i - 1]
        for j in range(1, m + 1):
            c = 0 if Ai == B[j - 1] else 1
            Fi[j] = min(Fprev[j] + 1, Fi[j - 1] + 1, Fprev[j - 1] + c)

    R = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        R[i][m] = n - i
    for j in range(m + 1):
        R[n][j] = m - j

    for i in range(n - 1, -1, -1):
        Ri = R[i]
        Rnext = R[i + 1]
        Ai = A[i]
        for j in range(m - 1, -1, -1):
            c = 0 if Ai == B[j] else 1
            Ri[j] = min(Rnext[j] + 1, Ri[j + 1] + 1, Rnext[j + 1] + c)

    OPT = F[n][m]
    max_cost = OPT + D
    out = []
    ca = []
    cb = []

    def dfs(i, j, g):
        if i == n and j == m:
            out.append(("".join(ca), "".join(cb)))
            return

        # 0: diag
        if i < n and j < m:
            g2 = g + (0 if A[i] == B[j] else 1)
            if g2 + R[i + 1][j + 1] <= max_cost:
                ca.append(A[i])
                cb.append(B[j])
                dfs(i + 1, j + 1, g2)
                ca.pop()
                cb.pop()

        # 1: down (gap in B)
        if i < n:
            g2 = g + 1
            if g2 + R[i + 1][j] <= max_cost:
                ca.append(A[i])
                cb.append('-')
                dfs(i + 1, j, g2)
                ca.pop()
                cb.pop()

        # 2: right (gap in A)
        if j < m:
            g2 = g + 1
            if g2 + R[i][j + 1] <= max_cost:
                ca.append('-')
                cb.append(B[j])
                dfs(i, j + 1, g2)
                ca.pop()
                cb.pop()

    dfs(0, 0, 0)
    out.sort()

    res = [str(len(out))]
    for p in out:
        res.append(p[0])
        res.append(p[1])
    sys.stdout.write("\n".join(res) + "\n")

if __name__ == "__main__":
    main()
