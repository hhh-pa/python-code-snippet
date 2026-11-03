import sys
import heapq

sys.setrecursionlimit(200000)

def bpm(u, reach, matchR, seen, n):
    for v in range(n):
        if u != v and reach[u][v] and not seen[v]:
            seen[v] = True
            if matchR[v] < 0 or bpm(matchR[v], reach, matchR, seen, n):
                matchR[v] = u
                return True
    return False

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
        
    idx = 2
    for _ in range(m):
        u = int(tokens[idx])
        v = int(tokens[idx+1])
        idx += 2
        reach[u][v] = True
        
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
                        
    hasse = []
    for u in range(n):
        for v in range(n):
            if u == v or not reach[u][v]:
                continue
            cover = True
            for w in range(n):
                if w != u and w != v and reach[u][w] and reach[w][v]:
                    cover = False
                    break
            if cover:
                hasse.append((u, v))
                
    hasse.sort()
    
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in hasse:
        adj[u].append(v)
        indeg[v] += 1
        
    avail = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(avail)
    
    topo = []
    while avail:
        u = heapq.heappop(avail)
        topo.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(avail, v)
                
    h = [1] * n
    for v in topo:
        for u in range(n):
            if u != v and reach[u][v]:
                if h[u] + 1 > h[v]:
                    h[v] = h[u] + 1
    height = max(h) if n > 0 else 0
    
    matchR = [-1] * n
    matching = 0
    for u in range(n):
        seen = [False] * n
        if bpm(u, reach, matchR, seen, n):
            matching += 1
            
    out = [str(len(hasse))]
    for u, v in hasse:
        out.append(f"{u} {v}")
    out.append(str(height))
    out.append(str(n - matching))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
