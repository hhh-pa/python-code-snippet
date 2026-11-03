import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    A = []
    for _ in range(n):
        A.append([int(x) for x in tokens[idx : idx + n]])
        idx += n
    B = []
    for _ in range(n):
        B.append([int(x) for x in tokens[idx : idx + n]])
        idx += n

    # Transpose B for fast row-row dot product
    B_T = list(zip(*B))
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        row_A = A[i]
        row_C = C[i]
        for j in range(n):
            col_B = B_T[j]
            row_C[j] = sum(x * y for x, y in zip(row_A, col_B))

    out = []
    for row in C:
        out.append(" ".join(map(str, row)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
