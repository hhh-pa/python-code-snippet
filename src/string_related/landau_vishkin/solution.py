import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    P = tokens[0]
    T = tokens[1]
    k = int(tokens[2])

    m = len(P)
    n = len(T)

    def lce(i, j):
        c = 0
        while i < m and j < n and P[i] == T[j]:
            i += 1
            j += 1
            c += 1
        return c

    NEG = -1000000000
    OFF = m + 2
    SZ = m + n + 5

    prev = [NEG] * SZ
    cur = [NEG] * SZ
    matched = [False] * n

    for d in range(k + 1):
        cur = [NEG] * SZ
        for e in range(-m, n + 1):
            if d == 0:
                if e < 0 or e > n:
                    continue
                r = 0
            else:
                a = prev[e + OFF] + 1
                b = prev[e - 1 + OFF]
                c = prev[e + 1 + OFF] + 1
                r = max(a, b, c)
                if r <= NEG // 2:
                    continue
            L = r + lce(r, r + e)
            cur[e + OFF] = L
            if L >= m:
                end = m + e - 1
                if 0 <= end < n:
                    matched[end] = True
        prev = cur

    ans = [j for j in range(n) if matched[j]]
    print(len(ans))
    if ans:
        print(" ".join(str(x) for x in ans))

if __name__ == "__main__":
    main()
