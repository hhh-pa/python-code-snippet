"""Multiprocessor makespan: list scheduling + LPT rule (CLRS 35)."""

import heapq
import sys


def _schedule(m, jobs):
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)
    best = 0
    for p in jobs:
        load, i = heapq.heappop(heap)
        load += p
        best = max(best, load)
        heapq.heappush(heap, (load, i))
    return best


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    m = data[0]
    n = data[1] if len(data) > 1 else 0
    jobs = data[2 : 2 + n]
    first = _schedule(m, jobs)
    lpt = _schedule(m, sorted(jobs, reverse=True))
    sys.stdout.write(f"{first}\n{lpt}")


if __name__ == "__main__":
    main()
