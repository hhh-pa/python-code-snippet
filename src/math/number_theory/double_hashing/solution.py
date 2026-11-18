"""Open-addressing hash table with double hashing (CLRS 11.4)."""

import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    m = data[0]
    n = data[1] if len(data) > 1 else 0
    keys = data[2 : 2 + n]
    table = [None] * m
    for k in keys:
        h1 = k % m
        h2 = 1 + (k % (m - 1))
        for i in range(m):
            j = (h1 + i * h2) % m
            if table[j] is None:
                table[j] = k
                break
    sys.stdout.write(" ".join("_" if v is None else str(v) for v in table))


if __name__ == "__main__":
    main()
