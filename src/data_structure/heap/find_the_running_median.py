import heapq
import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    max_heap = []  # stores -val
    min_heap = []  # stores val
    out = []

    for i in range(n):
        val = int(tokens[1 + i])
        if not max_heap or val <= -max_heap[0]:
            heapq.heappush(max_heap, -val)
        else:
            heapq.heappush(min_heap, val)

        # Rebalance
        if len(max_heap) > len(min_heap) + 1:
            heapq.heappush(min_heap, -heapq.heappop(max_heap))
        elif len(min_heap) > len(max_heap):
            heapq.heappush(max_heap, -heapq.heappop(min_heap))

        if len(max_heap) == len(min_heap):
            med = (-max_heap[0] + min_heap[0]) / 2.0
        else:
            med = float(-max_heap[0])
        out.append(f"{med:.1f}")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
