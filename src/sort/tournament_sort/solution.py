import heapq
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    heapq.heapify(nums)
    res = [heapq.heappop(nums) for _ in range(n)]
    sys.stdout.write("[" + ",".join(str(x) for x in res) + "]")

if __name__ == "__main__":
    main()
