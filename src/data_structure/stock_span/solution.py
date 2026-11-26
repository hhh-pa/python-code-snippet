"""Stock span problem (monotonic stack, O(n))."""

import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    p = data[1 : 1 + n]
    spans = [0] * n
    stack = []
    for i, x in enumerate(p):
        while stack and p[stack[-1]] <= x:
            stack.pop()
        spans[i] = i + 1 if not stack else i - stack[-1]
        stack.append(i)
    sys.stdout.write(" ".join(map(str, spans)))


if __name__ == "__main__":
    main()
