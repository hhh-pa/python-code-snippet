# https://leetcode.com/problems/sliding-window-maximum/
"""Sliding window maximum (monotonic deque, O(n))."""

import collections
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n, k = data[0], data[1]
    a = data[2 : 2 + n]
    dq = collections.deque()
    out = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        while dq[0] <= i - k:
            dq.popleft()
        if i + 1 >= k:
            out.append(str(a[dq[0]]))
    sys.stdout.write(" ".join(out))


if __name__ == "__main__":
    main()
