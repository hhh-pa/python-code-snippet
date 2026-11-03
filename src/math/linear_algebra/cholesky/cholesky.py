import math
import sys

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
        a.append([float(x) for x in tokens[idx : idx + n]])
        idx += n

    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j]
            for k in range(j):
                s -= L[i][k] * L[j][k]
            if i == j:
                if s <= 1e-9:
                    print("NOT_POSITIVE_DEFINITE")
                    return
                L[i][j] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]

    out = []
    for i in range(n):
        out.append(" ".join(f"{val:.6f}" for val in L[i]))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
