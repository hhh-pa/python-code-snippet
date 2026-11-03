import sys

def insertion_sort(a, lo, hi):
    for i in range(lo + 1, hi + 1):
        cur = a[i]
        j = i - 1
        while j >= lo and a[j] > cur:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur

def sift_down(a, start, end):
    root = start
    while (2 * root + 1) <= end:
        child = 2 * root + 1
        swap = root
        if a[swap] < a[child]:
            swap = child
        if child + 1 <= end and a[swap] < a[child + 1]:
            swap = child + 1
        if swap == root:
            return
        a[root], a[swap] = a[swap], a[root]
        root = swap

def heap_sort_range(a, lo, hi):
    n = hi - lo + 1
    # build max heap
    for start in range(n // 2 - 1, -1, -1):
        # map to lo
        root = lo + start
        # sift down within [lo, hi]
        r = root
        while (2 * (r - lo) + 1) < n:
            c = lo + 2 * (r - lo) + 1
            sw = r
            if a[sw] < a[c]:
                sw = c
            if c + 1 <= hi and a[sw] < a[c + 1]:
                sw = c + 1
            if sw == r:
                break
            a[r], a[sw] = a[sw], a[r]
            r = sw
    for end in range(hi, lo, -1):
        a[lo], a[end] = a[end], a[lo]
        # sift down root lo in [lo, end - 1]
        r = lo
        curr_len = end - lo
        while (2 * (r - lo) + 1) < curr_len:
            c = lo + 2 * (r - lo) + 1
            sw = r
            if a[sw] < a[c]:
                sw = c
            if c + 1 < end and a[sw] < a[c + 1]:
                sw = c + 1
            if sw == r:
                break
            a[r], a[sw] = a[sw], a[r]
            r = sw

def intro_sort(a):
    n = len(a)
    if n <= 1:
        return
    max_depth = 2 * (n.bit_length() - 1)
    
    def _introsort(lo, hi, depth):
        while hi - lo > 16:
            if depth == 0:
                heap_sort_range(a, lo, hi)
                return
            depth -= 1
            # median-of-three pivot
            mid = (lo + hi) // 2
            if a[mid] < a[lo]:
                a[lo], a[mid] = a[mid], a[lo]
            if a[hi] < a[lo]:
                a[lo], a[hi] = a[hi], a[lo]
            if a[hi] < a[mid]:
                a[mid], a[hi] = a[hi], a[mid]
            pivot = a[mid]
            
            i = lo
            j = hi
            while i <= j:
                while a[i] < pivot:
                    i += 1
                while a[j] > pivot:
                    j -= 1
                if i <= j:
                    a[i], a[j] = a[j], a[i]
                    i += 1
                    j -= 1
            if j - lo < hi - i:
                if lo < j:
                    _introsort(lo, j, depth)
                lo = i
            else:
                if i < hi:
                    _introsort(i, hi, depth)
                hi = j
        insertion_sort(a, lo, hi)

    _introsort(0, n - 1, max_depth)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    intro_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
