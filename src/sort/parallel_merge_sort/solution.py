import sys

sys.setrecursionlimit(200000)

def p_merge(A, p1, r1, p2, r2, B, p3):
    n1 = r1 - p1 + 1
    n2 = r2 - p2 + 1
    if n1 < n2:
        p_merge(A, p2, r2, p1, r1, B, p3)
        return
    if n1 <= 0:
        return
    if n2 <= 0:
        for i in range(n1):
            B[p3 + i] = A[p1 + i]
        return
    if n1 + n2 <= 64:
        i, j, k = p1, p2, p3
        while i <= r1 and j <= r2:
            if A[i] <= A[j]:
                B[k] = A[i]
                i += 1
            else:
                B[k] = A[j]
                j += 1
            k += 1
        while i <= r1:
            B[k] = A[i]
            i += 1
            k += 1
        while j <= r2:
            B[k] = A[j]
            j += 1
            k += 1
        return
    q1 = (p1 + r1) // 2
    lo, hi, q2 = p2, r2, r2 + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] < A[q1]:
            lo = mid + 1
        else:
            q2 = mid
            hi = mid - 1
    q3 = p3 + (q1 - p1) + (q2 - p2)
    B[q3] = A[q1]
    p_merge(A, p1, q1 - 1, p2, q2 - 1, B, p3)
    p_merge(A, q1 + 1, r1, q2, r2, B, q3 + 1)

def p_merge_sort(A, p, r, B, s):
    n = r - p + 1
    if n <= 64:
        A[p : r + 1] = sorted(A[p : r + 1])
        for i in range(p, r + 1):
            B[s + i - p] = A[i]
        return
    q = (p + r) // 2
    qp = s + (q - p + 1)
    p_merge_sort(A, p, q, B, s)
    p_merge_sort(A, q + 1, r, B, qp)
    p_merge(A, p, q, q + 1, r, B, s)
    for i in range(p, r + 1):
        A[i] = B[s + i - p]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 0:
        print("[]")
        return
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    aux = [0] * n
    p_merge_sort(a, 0, n - 1, aux, 0)
    sys.stdout.write("[" + ",".join(str(x) for x in a) + "]\n")

if __name__ == "__main__":
    main()
