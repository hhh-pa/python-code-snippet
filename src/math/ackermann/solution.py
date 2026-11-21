"""Ackermann function (exact closed forms for m <= 3)."""

import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = int(data[0]), int(data[1])
    if m == 0:
        ans = n + 1
    elif m == 1:
        ans = n + 2
    elif m == 2:
        ans = 2 * n + 3
    elif m == 3:
        ans = (1 << (n + 3)) - 3
    else:
        sys.stdout.write("TOO BIG")
        return
    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()
