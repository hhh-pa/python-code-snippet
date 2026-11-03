import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    n = int(tokens[1])
    if m <= 0 or n <= 0:
        return

    idx = 2
    A = []
    for _ in range(m):
        A.append([float(x) for x in tokens[idx : idx + n]])
        idx += n
    b = [float(x) for x in tokens[idx : idx + m]]

    # Normal equations: AtA x = Atb
    AtA = [[0.0] * n for _ in range(n)]
    Atb = [0.0] * n
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(m):
                s += A[k][i] * A[k][j]
            AtA[i][j] = s
        s = 0.0
        for k in range(m):
            s += A[k][i] * b[k]
        Atb[i] = s

    aug = []
    for i in range(n):
        aug.append(AtA[i] + [Atb[i]])

    for col in range(n):
        pivot = col
        best = abs(aug[col][col])
        for row in range(col + 1, n):
            val = abs(aug[row][col])
            if val > best:
                best = val
                pivot = row
        if best < 1e-12:
            print("SINGULAR")
            return
        if pivot != col:
            aug[pivot], aug[col] = aug[col], aug[pivot]

        col_row = aug[col]
        diag = col_row[col]
        for row in range(col + 1, n):
            row_r = aug[row]
            f = row_r[col] / diag
            for j in range(col, n + 1):
                row_r[j] -= f * col_row[j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = aug[i][n]
        for j in range(i + 1, n):
            s -= aug[i][j] * x[j]
        x[i] = s / aug[i][i]

    print(" ".join(f"{val:.6f}" for val in x))

if __name__ == '__main__':
    main()
