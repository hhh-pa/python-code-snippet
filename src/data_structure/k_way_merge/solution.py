"""K-way merge of sorted lists (heap, O(N log k))."""

import heapq
import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    pos = 0
    k = data[pos]
    pos += 1
    heap = []
    lists = []
    for i in range(k):
        m = data[pos] if pos < len(data) else 0
        pos += 1
        lst = data[pos : pos + m]
        pos += m
        lists.append(lst)
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    out = []
    while heap:
        v, i, j = heapq.heappop(heap)
        out.append(str(v))
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    sys.stdout.write(" ".join(out))


if __name__ == "__main__":
    main()
