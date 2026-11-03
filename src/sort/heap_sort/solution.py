import heapq
import sys

def heap_sort(nums):
    heapq.heapify(nums)
    return [heapq.heappop(nums) for _ in range(len(nums))]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    sorted_nums = heap_sort(nums) if n > 0 else []
    sys.stdout.write("[" + ",".join(str(x) for x in sorted_nums) + "]")

if __name__ == "__main__":
    main()
