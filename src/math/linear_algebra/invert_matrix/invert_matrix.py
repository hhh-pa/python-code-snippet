import sys

MOD = 1000000007

def mod_norm(x):
    r = x % MOD
    return r if r >= 0 else r + MOD

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n <= 0:
        return
    idx = 1
    aug = []
    for i in range(n):
        row = [mod_norm(int(x)) for x in tokens[idx : idx + n]]
        idx += n
        ident = [0] * n
        ident[i] = 1
        aug.append(row + ident)

    for col in range(n):
        pivot = -1
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            print("SINGULAR")
            return
        if pivot != col:
            aug[pivot], aug[col] = aug[col], aug[pivot]

        inv = pow(aug[col][col], MOD - 2, MOD)
        col_row = aug[col]
        for j in range(2 * n):
            col_row[j] = (col_row[j] * inv) % MOD

        for row in range(n):
            if row != col and aug[row][col] != 0:
                f = aug[row][col]
                row_r = aug[row]
                for j in range(2 * n):
                    row_r[j] = (row_r[j] - f * col_row[j]) % MOD

    out = []
    for i in range(n):
        out.append(" ".join(str(aug[i][n + j]) for j in range(n)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
