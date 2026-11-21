"""Lexicographic r-subsets of {1..n} (Brualdi Theorem 4.4.1)."""

import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, r = int(data[0]), int(data[1])
    cur = list(range(1, r + 1))
    last = list(range(n - r + 1, n + 1))
    out = [" ".join(map(str, cur))]
    while cur != last:
        present = set(cur)
        k = r - 1
        while not (cur[k] + 1 <= n and cur[k] + 1 not in present):
            k -= 1
        cur[k] += 1
        for j in range(k + 1, r):
            cur[j] = cur[j - 1] + 1
        out.append(" ".join(map(str, cur)))
    sys.stdout.write(str(len(out)) + "\n" + "\n".join(out))


if __name__ == "__main__":
    main()
