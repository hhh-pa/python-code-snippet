import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    p = [0.0] * (n + 1)
    q = [0.0] * (n + 1)
    idx = 1
    for i in range(1, n + 1):
        p[i] = float(tokens[idx])
        idx += 1
    for i in range(n + 1):
        q[i] = float(tokens[idx])
        idx += 1

    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    w = [[0.0] * (n + 2) for _ in range(n + 2)]

    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            best = 1e100
            for r in range(i, j + 1):
                c = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if c < best:
                    best = c
            e[i][j] = best

    print(f"{e[1][n]:.6f}")

if __name__ == '__main__':
    main()
