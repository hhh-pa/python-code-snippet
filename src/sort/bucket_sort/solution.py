import sys

def insertion_sort(a):
    for i in range(1, len(a)):
        cur = a[i]
        j = i - 1
        while j >= 0 and a[j] > cur:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur

def bucket_sort(nums, k=8):
    if not nums:
        return
    max_v = max(nums)
    min_v = min(nums)
    if max_v == min_v:
        return
    buckets = [[] for _ in range(k + 1)]
    diff = max_v - min_v
    for v in nums:
        idx = (v - min_v) * k // diff
        buckets[idx].append(v)
    pos = 0
    for b in buckets:
        insertion_sort(b)
        for v in b:
            nums[pos] = v
            pos += 1

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    if n > 0:
        bucket_sort(nums, 8)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
