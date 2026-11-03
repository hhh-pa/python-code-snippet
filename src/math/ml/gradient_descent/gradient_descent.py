import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    A = []
    for _ in range(n):
        A.append([float(x) for x in tokens[idx : idx + n]])
        idx += n
    b = [float(x) for x in tokens[idx : idx + n]]
    idx += n
    x = [float(x) for x in tokens[idx : idx + n]]
    idx += n
    lr = float(tokens[idx])
    iters = int(tokens[idx + 1])

    for _ in range(iters):
        g = [0.0] * n
        for i in range(n):
            s = 0.0
            Ai = A[i]
            for j in range(n):
                s += Ai[j] * x[j]
            g[i] = 2.0 * s + b[i]
        for i in range(n):
            x[i] -= lr * g[i]

    f = 0.0
    for i in range(n):
        Ai = A[i]
        xi = x[i]
        for j in range(n):
            f += xi * Ai[j] * x[j]
        f += b[i] * xi

    out_x = " ".join(f"{xi + 0.0:.6f}" for xi in x)
    print(out_x)
    print(f"{f + 0.0:.6f}")

if __name__ == '__main__':
    main()
