import sys

sys.setrecursionlimit(200000)

def chrom(n, edges, k):
    s = set()
    for u, v in edges:
        a = min(u, v)
        b = max(u, v)
        if a != b:
            s.add((a, b))
    es = sorted(s)
    if not es:
        return k ** n
    u, v = es[0]
    rest = es[1:]
    p1 = chrom(n, rest, k)
    
    mp = [-1] * n
    nxt = 0
    for i in range(n):
        if i == v:
            continue
        mp[i] = nxt
        nxt += 1
        
    ne = []
    for a, b in rest:
        na = mp[u] if a == v else mp[a]
        nb = mp[u] if b == v else mp[b]
        if na != nb:
            ne.append((na, nb))
            
    return p1 - chrom(n - 1, ne, k)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    k = int(tokens[2])
    idx = 3
    edges = []
    for _ in range(m):
        u = int(tokens[idx])
        v = int(tokens[idx+1])
        idx += 2
        edges.append((u, v))
        
    sys.stdout.write(str(chrom(n, edges, k)) + "\n")

if __name__ == "__main__":
    main()
