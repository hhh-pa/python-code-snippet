import collections
import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    k = int(tokens[1])
    if n <= 0 or k <= 0 or k > n:
        return

    a = [int(tokens[2 + i]) for i in range(n)]

    max_dq = collections.deque()
    min_dq = collections.deque()
    max_out = []
    min_out = []

    for i in range(n):
        while max_dq and max_dq[0] <= i - k:
            max_dq.popleft()
        while max_dq and a[max_dq[-1]] <= a[i]:
            max_dq.pop()
        max_dq.append(i)

        while min_dq and min_dq[0] <= i - k:
            min_dq.popleft()
        while min_dq and a[min_dq[-1]] >= a[i]:
            min_dq.pop()
        min_dq.append(i)

        if i >= k - 1:
            max_out.append(str(a[max_dq[0]]))
            min_out.append(str(a[min_dq[0]]))

    sys.stdout.write(" ".join(max_out) + "\n")
    sys.stdout.write(" ".join(min_out) + "\n")


if __name__ == "__main__":
    main()
