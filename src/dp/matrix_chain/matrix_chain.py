import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    d = [int(tokens[1 + i]) for i in range(n + 1)]
    if n <= 1:
        print(0)
        return

    INF = float('inf')
    m = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = INF
            di = d[i]
            dj1 = d[j + 1]
            mi = m[i]
            for k in range(i, j):
                cost = mi[k] + m[k + 1][j] + di * d[k + 1] * dj1
                if cost < best:
                    best = cost
            mi[j] = best

    print(m[0][n - 1])

if __name__ == '__main__':
    main()
