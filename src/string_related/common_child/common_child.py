import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    A = tokens[0]
    B = tokens[1]
    n = len(A)
    m = len(B)

    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        a_char = A[i - 1]
        for j in range(1, m + 1):
            if a_char == B[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = prev[j] if prev[j] > curr[j - 1] else curr[j - 1]
        prev, curr = curr, prev

    print(prev[m])

if __name__ == "__main__":
    main()
