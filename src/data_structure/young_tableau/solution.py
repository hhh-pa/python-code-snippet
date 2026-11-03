import sys

INF = 4000000000000000000


class Young:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.a = [[INF] * n for _ in range(m)]

    def insert(self, x):
        m, n = self.m, self.n
        a = self.a
        if a[m - 1][n - 1] != INF:
            return False
        i, j = m - 1, n - 1
        a[i][j] = x
        while i > 0 or j > 0:
            bi, bj = i, j
            if i > 0 and a[i - 1][j] > a[bi][bj]:
                bi, bj = i - 1, j
            if j > 0 and a[i][j - 1] > a[bi][bj]:
                bi, bj = i, j - 1
            if bi == i and bj == j:
                break
            a[i][j], a[bi][bj] = a[bi][bj], a[i][j]
            i, j = bi, bj
        return True

    def extract_min(self):
        m, n = self.m, self.n
        a = self.a
        if a[0][0] == INF:
            return None
        res = a[0][0]
        i, j = 0, 0
        a[0][0] = INF
        while True:
            si, sj = i, j
            if i + 1 < m and a[i + 1][j] < a[si][sj]:
                si, sj = i + 1, j
            if j + 1 < n and a[i][j + 1] < a[si][sj]:
                si, sj = i, j + 1
            if si == i and sj == j:
                break
            a[i][j] = a[si][sj]
            a[si][sj] = INF
            i, j = si, sj
        return res

    def search(self, x):
        m, n = self.m, self.n
        a = self.a
        i, j = 0, n - 1
        while i < m and j >= 0:
            val = a[i][j]
            if val == x:
                return True
            if val > x:
                j -= 1
            else:
                i += 1
        return False


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    n = int(tokens[1])
    q = int(tokens[2])
    idx = 3
    t = Young(m, n)
    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            if not t.insert(x):
                out.append("FULL")
        elif op == 2:
            res = t.extract_min()
            out.append(str(res) if res is not None else "EMPTY")
        elif op == 3:
            x = int(tokens[idx])
            idx += 1
            out.append("YES" if t.search(x) else "NO")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
