import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s1 = tokens[0]
    s2 = tokens[1]
    n = len(s1)
    m = len(s2)

    NEG = -10**9
    MATCH = 2
    MISMATCH = -1
    GAP_OPEN = -2
    GAP_EXTEND = -1

    M = [[NEG] * (m + 1) for _ in range(n + 1)]
    Ix = [[NEG] * (m + 1) for _ in range(n + 1)]
    Iy = [[NEG] * (m + 1) for _ in range(n + 1)]

    M[0][0] = 0
    for i in range(1, n + 1):
        Ix[i][0] = GAP_OPEN + (i - 1) * GAP_EXTEND
    for j in range(1, m + 1):
        Iy[0][j] = GAP_OPEN + (j - 1) * GAP_EXTEND

    for i in range(1, n + 1):
        Mi = M[i]
        Mprev = M[i - 1]
        Ixi = Ix[i]
        Ixprev = Ix[i - 1]
        Iyi = Iy[i]
        Iyprev = Iy[i - 1]
        s1_char = s1[i - 1]

        for j in range(1, m + 1):
            sc = MATCH if s1_char == s2[j - 1] else MISMATCH
            best_diag = max(Mprev[j - 1], Ixprev[j - 1], Iyprev[j - 1])
            Mi[j] = best_diag + sc
            Ixi[j] = max(Mprev[j] + GAP_OPEN, Ixprev[j] + GAP_EXTEND)
            Iyi[j] = max(Mi[j - 1] + GAP_OPEN, Iyi[j - 1] + GAP_EXTEND)

    print(max(M[n][m], Ix[n][m], Iy[n][m]))

if __name__ == "__main__":
    main()
