import sys

def counting_sort(nums):
    if not nums:
        return nums
    max_v = max(nums)
    cnt = [0] * (max_v + 1)
    for v in nums:
        cnt[v] += 1
    idx = 0
    for v, c in enumerate(cnt):
        for _ in range(c):
            nums[idx] = v
            idx += 1
    return nums

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    if n > 0:
        counting_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
