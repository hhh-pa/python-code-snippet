from collections import deque
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    k = int(tokens[0])
    m = int(tokens[1])
    rq = [int(x) for x in tokens[2 : 2 + m]]
    if k <= 0:
        print(m)
        return

    INF = 10**9
    # Build occurrences queue for each page
    q = {}
    for i, p in enumerate(rq):
        if p not in q:
            q[p] = deque()
        q[p].append(i)

    cache = set()
    faults = 0

    for p in rq:
        q[p].popleft()
        if p in cache:
            continue
        faults += 1
        if len(cache) < k:
            cache.add(p)
            continue
        # Find candidate with farthest next use
        best = 0
        bestn = -1
        first = True
        for c in cache:
            nu = q[c][0] if q[c] else INF
            if first or nu > bestn or (nu == bestn and c < best):
                best = c
                bestn = nu
                first = False
        cache.remove(best)
        cache.add(p)

    print(faults)

if __name__ == '__main__':
    main()
