"""Large Schroder numbers via small-number recurrence (Brualdi 8.5)."""

import sys


def _small(upto):
    s = [0] * (upto + 1)
    s[1] = 1
    for n in range(2, upto + 1):
        s[n] = 2 * sum(s[j] * s[n - j] for j in range(1, n)) - s[n - 1]
    return s


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    q = data[0]
    ns = data[1 : 1 + q]
    s = _small(max(ns) + 1) if ns else [0]
    out = []
    for n in ns:
        out.append("1" if n == 0 else str(2 * s[n + 1]))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
