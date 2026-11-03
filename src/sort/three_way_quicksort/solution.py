import sys

sys.setrecursionlimit(200000)

def sort3(a, lo, hi):
    if lo >= hi:
        return
    pivot = a[lo + (hi - lo) // 2]
    lt = lo
    gt = hi
    i = lo
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    sort3(a, lo, lt - 1)
    sort3(a, gt + 1, hi)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    if nums:
        sort3(nums, 0, len(nums) - 1)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
