import sys

sys.setrecursionlimit(200000)

def insertion_sort(a, l, r):
    for i in range(l + 1, r + 1):
        key = a[i]
        j = i - 1
        while j >= l and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def median_idx(a, l, r):
    insertion_sort(a, l, r)
    return l + (r - l) // 2

def bfprt_select(a, l, r, k):
    if l == r:
        return a[l]
    n = r - l + 1
    num_groups = (n + 4) // 5
    medians = []
    for i in range(num_groups):
        gl = l + i * 5
        gr = min(l + (i + 1) * 5 - 1, r)
        mi = median_idx(a, gl, gr)
        medians.append(a[mi])
    
    if len(medians) == 1:
        pivot = medians[0]
    else:
        medians.sort()
        pivot = medians[len(medians) // 2]
    
    lt = l
    gt = r
    i = l
    while i <= gt:
        if a[i] < pivot:
            a[i], a[lt] = a[lt], a[i]
            i += 1
            lt += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
            
    rank_lt = lt - l
    rank_eq = gt - lt + 1
    if k < rank_lt:
        return bfprt_select(a, l, lt - 1, k)
    elif k < rank_lt + rank_eq:
        return pivot
    else:
        return bfprt_select(a, gt + 1, r, k - rank_lt - rank_eq)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 0:
        print(0)
        return
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    k = int(tokens[1 + n])
    k -= 1
    if k < 0 or k >= n:
        print(0)
        return
    print(bfprt_select(a, 0, n - 1, k))

if __name__ == "__main__":
    main()
