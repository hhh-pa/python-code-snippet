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
    a = []
    for _ in range(n):
        a.append([mod_norm(int(x)) for x in tokens[idx : idx + n]])
        idx += n
    b = [mod_norm(int(x)) for x in tokens[idx : idx + n]]

    pi = list(range(n))
    swaps = 0

    for k in range(n):
        p = 0
        kp = k
        for i in range(k, n):
            if a[i][k] > p:
                p = a[i][k]
                kp = i
        if p == 0:
            print("SINGULAR")
            return
        if kp != k:
            swaps += 1
            pi[k], pi[kp] = pi[kp], pi[k]
            a[k], a[kp] = a[kp], a[k]

        inv = pow(a[k][k], MOD - 2, MOD)
        for i in range(k + 1, n):
            a[i][k] = (a[i][k] * inv) % MOD
            factor = a[i][k]
            row_i = a[i]
            row_k = a[k]
            for j in range(k + 1, n):
                row_i[j] = (row_i[j] - factor * row_k[j]) % MOD

    det = 1
    for k in range(n):
        det = (det * a[k][k]) % MOD
    if (swaps & 1) and det:
        det = MOD - det

    # Solve Ly = Pb
    y = [0] * n
    for i in range(n):
        s = b[pi[i]]
        for j in range(i):
            s = (s - a[i][j] * y[j]) % MOD
        y[i] = s

    # Solve Ux = y
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s = (s - a[i][j] * x[j]) % MOD
        x[i] = (s * pow(a[i][i], MOD - 2, MOD)) % MOD

    # Inverse
    inv_mat = [[0] * n for _ in range(n)]
    for c in range(n):
        # e has 1 at position c
        yy = [0] * n
        for i in range(n):
            s = 1 if pi[i] == c else 0
            for j in range(i):
                s = (s - a[i][j] * yy[j]) % MOD
            yy[i] = s
        col = [0] * n
        for i in range(n - 1, -1, -1):
            s = yy[i]
            for j in range(i + 1, n):
                s = (s - a[i][j] * col[j]) % MOD
            col[i] = (s * pow(a[i][i], MOD - 2, MOD)) % MOD
        for r in range(n):
            inv_mat[r][c] = col[r]

    print(det)
    print(*(x))
    out = []
    for r in range(n):
        out.append(" ".join(str(val) for val in inv_mat[r]))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
