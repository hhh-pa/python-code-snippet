import sys

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
    S = int(tokens[1])
    idx = 2
    a = []
    for _ in range(n):
        row = [int(tokens[idx + j]) for j in range(n)]
        idx += n
        a.append(row)
        
    terms = []
    while True:
        any_pos = any(a[i][j] > 0 for i in range(n) for j in range(n))
        if not any_pos:
            break
            
        adj = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if a[i][j] > 0:
                    adj[i].append(j)
                    
        matchR = [-1] * n
        for u in range(n):
            seen = [False] * n
            bpm(u, adj, matchR, seen)
            
        ml = [-1] * n
        for v in range(n):
            if matchR[v] >= 0:
                ml[matchR[v]] = v
                
        c = -1
        for i in range(n):
            if c < 0 or a[i][ml[i]] < c:
                c = a[i][ml[i]]
                
        for i in range(n):
            a[i][ml[i]] -= c
            
        line = str(c) + " " + " ".join(map(str, ml))
        terms.append(line)
        
    sys.stdout.write(str(len(terms)) + "\n")
    for t in terms:
        sys.stdout.write(t + "\n")

if __name__ == "__main__":
    main()
