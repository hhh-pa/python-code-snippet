import sys

sys.setrecursionlimit(200000)

def quick_sort(a):
    def _sort(lo, hi):
        if lo >= hi:
            return
        pivot = a[(lo + hi) // 2]
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
        _sort(lo, lt - 1)
        _sort(gt + 1, hi)
    if len(a) > 1:
        _sort(0, len(a) - 1)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    quick_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
