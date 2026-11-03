import sys

def insertion_sort(nums):
    for i in range(1, len(nums)):
        cur = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > cur:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = cur

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    insertion_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
