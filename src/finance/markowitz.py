import sys

def solve(A, b):
    n = len(A)
    A = [row[:] for row in A]
    b = list(b)
    for k in range(n):
        piv = k
        best = abs(A[k][k])
        for i in range(k + 1, n):
            if abs(A[i][k]) > best:
                best = abs(A[i][k])
                piv = i
        A[k], A[piv] = A[piv], A[k]
        b[k], b[piv] = b[piv], b[k]
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
            b[i] -= f * b[k]
    x = [0.0] * n
    for k in range(n - 1, -1, -1):
        s = b[k]
        for j in range(k + 1, n):
            s -= A[k][j] * x[j]
        x[k] = s / A[k][k]
    return x

def inverse(A):
    n = len(A)
    A = [row[:] for row in A]
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(n):
        piv = k
        best = abs(A[k][k])
        for i in range(k + 1, n):
            if abs(A[i][k]) > best:
                best = abs(A[i][k])
                piv = i
        A[k], A[piv] = A[piv], A[k]
        I[k], I[piv] = I[piv], I[k]
        d = A[k][k]
        for j in range(n):
            A[k][j] /= d
            I[k][j] /= d
        for i in range(n):
            if i == k:
                continue
            f = A[i][k]
            for j in range(n):
                A[i][j] -= f * A[k][j]
                I[i][j] -= f * I[k][j]
    return I

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    mu = [float(tokens[idx + i]) for i in range(n)]
    idx += n
    S = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            S[i][j] = float(tokens[idx])
            idx += 1
    rf = float(tokens[idx])
    idx += 1
    tg = [float(tokens[idx + i]) for i in range(3)]
    idx += 3
    tau = float(tokens[idx])
    idx += 1
    P = [float(tokens[idx + i]) for i in range(n)]
    idx += n
    Q = float(tokens[idx])
    om = float(tokens[idx + 1])
    idx += 2
    
    # min variance
    A = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            A[i][j] = S[i][j]
        A[i][n] = 1.0
        A[n][i] = 1.0
    b = [0.0] * (n + 1)
    b[n] = 1.0
    sol = solve(A, b)
    
    # tangency
    ex = [mu[i] - rf for i in range(n)]
    tw = solve(S, ex)
    ts = sum(tw)
    tw = [x / ts for x in tw]
    
    # frontier
    fvar = [0.0] * 3
    for f in range(3):
        F = [[0.0] * (n + 2) for _ in range(n + 2)]
        for i in range(n):
            for j in range(n):
                F[i][j] = S[i][j]
            F[i][n] = mu[i]
            F[n][i] = mu[i]
            F[i][n + 1] = 1.0
            F[n + 1][i] = 1.0
        fb = [0.0] * (n + 2)
        fb[n] = tg[f]
        fb[n + 1] = 1.0
        w = solve(F, fb)
        v = sum(w[i] * S[i][j] * w[j] for i in range(n) for j in range(n))
        fvar[f] = v
        
    # Black-Litterman
    tS = [[S[i][j] * tau for j in range(n)] for i in range(n)]
    iTS = inverse(tS)
    M = [[iTS[i][j] + P[i] * P[j] / om for j in range(n)] for i in range(n)]
    rhs = [0.0] * n
    for i in range(n):
        s = sum(iTS[i][j] * mu[j] for j in range(n))
        rhs[i] = s + P[i] * Q / om
    iM = inverse(M)
    bl = [sum(iM[i][j] * rhs[j] for j in range(n)) for i in range(n)]
    
    minvar_str = " ".join(f"{sol[i]:.6f}" for i in range(n))
    sys.stdout.write(f"MINVAR: {minvar_str}\n")
    tangency_str = " ".join(f"{x:.6f}" for x in tw)
    sys.stdout.write(f"TANGENCY: {tangency_str}\n")
    frontier_str = " ".join(f"{tg[f]:.6f},{fvar[f]:.6f}" for f in range(3))
    sys.stdout.write(f"FRONTIER: {frontier_str}\n")
    bl_str = " ".join(f"{x:.6f}" for x in bl)
    sys.stdout.write(f"BL: {bl_str}\n")

if __name__ == "__main__":
    main()
