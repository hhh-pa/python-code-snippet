import bisect
import sys

def longest_increasing_subsequence(arr):
    if not arr:
        return 0
    tails = []
    for x in arr:
        it = bisect.bisect_left(tails, x)
        if it == len(tails):
            tails.append(x)
        else:
            tails[it] = x
    return len(tails)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    arr = [int(tokens[1 + i]) for i in range(n)]
    print(longest_increasing_subsequence(arr))

if __name__ == '__main__':
    main()
