# https://www.hackerrank.com/challenges/largest-rectangle/problem
"""Largest rectangle in a histogram (monotonic stack, O(n))."""

import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    h = data[1 : 1 + n]
    best = 0
    stack = []
    for i, x in enumerate([*h, 0]):
        while stack and h[stack[-1]] > x:
            height = h[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            area = height * width
            if area > best:
                best = area
        stack.append(i)
    sys.stdout.write(str(best))


if __name__ == "__main__":
    main()
