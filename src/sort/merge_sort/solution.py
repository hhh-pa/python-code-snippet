import sys

def merge(nums, l, m, r, aux):
    i = l
    j = m + 1
    k = l
    while i <= m and j <= r:
        if nums[i] <= nums[j]:
            aux[k] = nums[i]
            i += 1
        else:
            aux[k] = nums[j]
            j += 1
        k += 1
    while i <= m:
        aux[k] = nums[i]
        i += 1
        k += 1
    while j <= r:
        aux[k] = nums[j]
        j += 1
        k += 1
    for idx in range(l, r + 1):
        nums[idx] = aux[idx]

def sort_rec(nums, l, r, aux):
    if l < r:
        m = (l + r) // 2
        sort_rec(nums, l, m, aux)
        sort_rec(nums, m + 1, r, aux)
        merge(nums, l, m, r, aux)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    if n > 0:
        aux = [0] * n
        sort_rec(nums, 0, n - 1, aux)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
