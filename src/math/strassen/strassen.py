import sys

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def standard_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            aik = Ai[k]
            Bk = B[k]
            for j in range(n):
                Ci[j] += aik * Bk[j]
    return C

def strassen(A, B):
    n = len(A)
    if n <= 2:
        return standard_mult(A, B)

    k = n // 2
    a11 = [[A[i][j] for j in range(k)] for i in range(k)]
    a12 = [[A[i][j + k] for j in range(k)] for i in range(k)]
    a21 = [[A[i + k][j] for j in range(k)] for i in range(k)]
    a22 = [[A[i + k][j + k] for j in range(k)] for i in range(k)]

    b11 = [[B[i][j] for j in range(k)] for i in range(k)]
    b12 = [[B[i][j + k] for j in range(k)] for i in range(k)]
    b21 = [[B[i + k][j] for j in range(k)] for i in range(k)]
    b22 = [[B[i + k][j + k] for j in range(k)] for i in range(k)]

    m1 = strassen(add(a11, a22), add(b11, b22))
    m2 = strassen(add(a21, a22), b11)
    m3 = strassen(a11, sub(b12, b22))
    m4 = strassen(a22, sub(b21, b11))
    m5 = strassen(add(a11, a12), b22)
    m6 = strassen(sub(a21, a11), add(b11, b12))
    m7 = strassen(sub(a12, a22), add(b21, b22))

    c11 = add(sub(add(m1, m4), m5), m7)
    c12 = add(m3, m5)
    c21 = add(m2, m4)
    c22 = add(add(sub(m1, m2), m3), m6)

    C = [[0] * n for _ in range(n)]
    for i in range(k):
        Ci = C[i]
        Cik = C[i + k]
        c11i = c11[i]
        c12i = c12[i]
        c21i = c21[i]
        c22i = c22[i]
        for j in range(k):
            Ci[j] = c11i[j]
            Ci[j + k] = c12i[j]
            Cik[j] = c21i[j]
            Cik[j + k] = c22i[j]
    return C

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])

    m = 1
    while m < n:
        m <<= 1

    A = [[0] * m for _ in range(m)]
    B = [[0] * m for _ in range(m)]

    idx = 1
    for i in range(n):
        for j in range(n):
            A[i][j] = int(tokens[idx])
            idx += 1

    for i in range(n):
        for j in range(n):
            B[i][j] = int(tokens[idx])
            idx += 1

    C = strassen(A, B)

    out = []
    for i in range(n):
        out.append(" ".join(str(C[i][j]) for j in range(n)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
