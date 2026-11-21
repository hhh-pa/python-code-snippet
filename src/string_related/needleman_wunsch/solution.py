import sys


def main():
    toks = sys.stdin.read().strip().split(" ")
    if len(toks) < 4:
        return
    match, mismatch, gap = (int(toks[1]), int(toks[2]), int(toks[3]))
    s1 = toks[4] if len(toks) > 4 else ""
    s2 = toks[5] if len(toks) > 5 else ""
    n, m = len(s1), len(s2)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        f[i][0] = i * gap
    for j in range(1, m + 1):
        f[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = match if s1[i - 1] == s2[j - 1] else mismatch
            f[i][j] = max(f[i - 1][j - 1] + sub, f[i - 1][j] + gap, f[i][j - 1] + gap)
    a1, a2 = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            sub = match if s1[i - 1] == s2[j - 1] else mismatch
            if f[i][j] == f[i - 1][j - 1] + sub:
                a1.append(s1[i - 1])
                a2.append(s2[j - 1])
                i -= 1
                j -= 1
                continue
        if i > 0 and f[i][j] == f[i - 1][j] + gap:
            a1.append(s1[i - 1])
            a2.append("-")
            i -= 1
        else:
            a1.append("-")
            a2.append(s2[j - 1])
            j -= 1
    sys.stdout.write(f"{f[n][m]}\n{''.join(reversed(a1))}\n{''.join(reversed(a2))}")


if __name__ == "__main__":
    main()
