import sys
import math

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    es = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        p = int(next(it))
        q = int(next(it))
        w = -math.log(float(p) / float(q))
        es.append((u, v, w))

    d = [0.0] * n
    for _ in range(n):
        for u, v, w in es:
            if d[u] + w < d[v]:
                d[v] = d[u] + w

    for u, v, w in es:
        if d[u] + w < d[v]:
            print("ARBITRAGE")
            return

    print("NO ARBITRAGE")

if __name__ == "__main__":
    main()
