import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n <= 0:
        return

    idx = 1
    if n == 1:
        diag = [float(tokens[idx])]
        rhs = [float(tokens[idx + 1])]
        lo = []
        hi = []
    else:
        lo = [float(tokens[idx + i]) for i in range(n - 1)]
        idx += n - 1
        diag = [float(tokens[idx + i]) for i in range(n)]
        idx += n
        hi = [float(tokens[idx + i]) for i in range(n - 1)]
        idx += n - 1
        rhs = [float(tokens[idx + i]) for i in range(n)]
        idx += n

    # Thomas algorithm: forward elimination
    cp = [0.0] * max(0, n - 1)
    dp = [0.0] * n
    if n == 1:
        if abs(diag[0]) < 1e-12:
            print("SINGULAR")
            return
        dp[0] = rhs[0] / diag[0]
    else:
        if abs(diag[0]) < 1e-12:
            print("SINGULAR")
            return
        cp[0] = hi[0] / diag[0]
        dp[0] = rhs[0] / diag[0]
        for i in range(1, n - 1):
            denom = diag[i] - lo[i - 1] * cp[i - 1]
            if abs(denom) < 1e-12:
                print("SINGULAR")
                return
            cp[i] = hi[i] / denom
            dp[i] = (rhs[i] - lo[i - 1] * dp[i - 1]) / denom
        denom = diag[n - 1] - lo[n - 2] * cp[n - 2]
        if abs(denom) < 1e-12:
            print("SINGULAR")
            return
        dp[n - 1] = (rhs[n - 1] - lo[n - 2] * dp[n - 2]) / denom

    # Back substitution
    x = [0.0] * n
    if n == 1:
        x[0] = dp[0]
    else:
        x[n - 1] = dp[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = dp[i] - cp[i] * x[i + 1]

    print(" ".join(f"{val:.6f}" for val in x))

if __name__ == '__main__':
    main()
