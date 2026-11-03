import sys

def partition(a, l, r):
    pivot = a[r]
    i = l
    for j in range(l, r):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[r] = a[r], a[i]
    return i

def quickselect(a, l, r, k):
    while l <= r:
        p = partition(a, l, r)
        if p == k:
            return a[p]
        elif p < k:
            l = p + 1
        else:
            r = p - 1
    return a[k]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    arr = [int(tokens[i]) for i in range(1, 1 + n)]
    ans = quickselect(arr, 0, n - 1, n // 2)
    print(ans)

if __name__ == "__main__":
    main()
