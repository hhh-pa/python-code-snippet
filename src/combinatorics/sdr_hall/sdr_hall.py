import sys

sys.setrecursionlimit(200000)

def bpm(u, adj, matchR, seen):
    for v in adj[u]:
        if seen[v]:
            continue
        seen[v] = True
        if matchR[v] < 0 or bpm(matchR[v], adj, matchR, seen):
            matchR[v] = u
            return True
    return False

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    e = int(tokens[2])
    
    adj = [[] for _ in range(n)]
    idx = 3
    for _ in range(e):
        u = int(tokens[idx])
        v = int(tokens[idx+1])
        idx += 2
        adj[u].append(v)
        
    for u in range(n):
        adj[u].sort()
        
    matchR = [-1] * m
    for u in range(n):
        seen = [False] * m
        bpm(u, adj, matchR, seen)
        
    matchL = [-1] * n
    for v in range(m):
        if matchR[v] >= 0:
            matchL[matchR[v]] = v
            
    for u in range(n):
        if matchL[u] < 0:
            sys.stdout.write("NO\n")
            return
            
    for u in range(n):
        sys.stdout.write(f"{u} {matchL[u]}\n")

if __name__ == "__main__":
    main()
