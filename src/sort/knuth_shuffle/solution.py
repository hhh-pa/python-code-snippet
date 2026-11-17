# https://leetcode.com/problems/shuffle-an-array/
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if len(data) < 2 or data[1] < 0:
        return
    seed, n = data[0], data[1]
    a = data[2:2 + n]
    a += [0] * (n - len(a))
    state = seed % 2147483648
    for i in range(n - 1, 0, -1):
        state = (1103515245 * state + 12345) % 2147483648
        j = state % (i + 1)
        a[i], a[j] = a[j], a[i]
    print('[' + ','.join(map(str, a)) + ']')


if __name__ == '__main__':
    main()
