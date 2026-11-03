import sys

def ins_run(a, lo, hi):
    for i in range(lo + 1, hi):
        cur = a[i]
        j = i - 1
        while j >= lo and a[j] > cur:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur

def merge_runs(a, lo, mid, hi, buf):
    i = lo
    j = mid
    k = lo
    while i < mid and j < hi:
        if a[i] <= a[j]:
            buf[k] = a[i]
            i += 1
        else:
            buf[k] = a[j]
            j += 1
        k += 1
    while i < mid:
        buf[k] = a[i]
        i += 1
        k += 1
    while j < hi:
        buf[k] = a[j]
        j += 1
        k += 1
    for t in range(lo, hi):
        a[t] = buf[t]

def tim_sort(a):
    n = len(a)
    if n < 2:
        return
    min_run = 32
    buf = [0] * n
    for lo in range(0, n, min_run):
        hi = min(lo + min_run, n)
        ins_run(a, lo, hi)
    sz = min_run
    while sz < n:
        for lo in range(0, n - sz, 2 * sz):
            mid = lo + sz
            hi = min(lo + 2 * sz, n)
            if a[mid - 1] <= a[mid]:
                continue
            merge_runs(a, lo, mid, hi, buf)
        sz *= 2

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    tim_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
