import sys

def radix_counting_sort(nums, exp):
    count = [[] for _ in range(10)]
    for num in nums:
        digit = (num // exp) % 10
        count[digit].append(num)
    k = 0
    for b in count:
        for v in b:
            nums[k] = v
            k += 1

def radix_sort(nums):
    if not nums:
        return
    m = max(nums)
    exp = 1
    while exp <= m:
        radix_counting_sort(nums, exp)
        exp *= 10

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    radix_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
