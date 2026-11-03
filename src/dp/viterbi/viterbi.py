import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    adj = [[] for _ in range(n)]
    idx = 2
    for _ in range(m):
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        p = float(tokens[idx + 2])
        idx += 3
        adj[u].append((v, p))

    s = int(tokens[idx])
    t = int(tokens[idx + 1])

    NEG = -1e100
    best = [NEG] * n
    best[s] = 0.0

    for u in range(n):
        if best[u] == NEG:
            continue
        bu = best[u]
        for v, p in adj[u]:
            if p > 0:
                c = bu + math.log(p)
                if c > best[v]:
                    best[v] = c

    if best[t] == NEG:
        print(f"{-1.0:.6f}")
    else:
        print(f"{best[t]:.6f}")

if __name__ == '__main__':
    main()
