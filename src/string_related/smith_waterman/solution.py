import sys


def main():
    toks = sys.stdin.read().strip().split(" ")
    if len(toks) < 6:
        return
    match, mismatch, gap = (int(toks[1]), int(toks[2]), int(toks[3]))
    s1, s2 = toks[4], toks[5]
    n, m = len(s1), len(s2)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    best, bi, bj = 0, 0, 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = match if s1[i - 1] == s2[j - 1] else mismatch
            f[i][j] = max(
                0, f[i - 1][j - 1] + sub, f[i - 1][j] + gap, f[i][j - 1] + gap
            )
            if f[i][j] > best:
                best, bi, bj = f[i][j], i, j
    a1, a2 = [], []
    i, j = bi, bj
    while i > 0 and j > 0 and f[i][j] > 0:
        sub = match if s1[i - 1] == s2[j - 1] else mismatch
        if f[i][j] == f[i - 1][j - 1] + sub:
            a1.append(s1[i - 1])
            a2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif f[i][j] == f[i - 1][j] + gap:
            a1.append(s1[i - 1])
            a2.append("-")
            i -= 1
        elif f[i][j] == f[i][j - 1] + gap:
            a1.append("-")
            a2.append(s2[j - 1])
            j -= 1
        else:
            break
    a1s, a2s = "".join(reversed(a1)), "".join(reversed(a2))
    sys.stdout.write(f"{best}\n{a1s}\n{a2s}" if a1s or a2s else f"{best}")


if __name__ == "__main__":
    main()
