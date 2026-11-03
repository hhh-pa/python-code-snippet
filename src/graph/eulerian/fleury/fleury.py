import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    
    adj = [[] for _ in range(n)]
    for i in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append((v, i))
        adj[v].append((u, i))
        
    odd = [i for i in range(n) if len(adj[i]) % 2 == 1]
    if len(odd) != 0 and len(odd) != 2:
        print("NO EULERIAN TRAIL")
        return
        
    src = -1
    for i in range(n):
        if adj[i]:
            src = i
            break
            
    if src == -1:
        print(0)
        return
        
    alive = [True] * m
    visited = [False] * n
    visited[src] = True
    st = [src]
    while st:
        u = st.pop()
        for w, e in adj[u]:
            if not visited[w]:
                visited[w] = True
                st.append(w)
                
    for i in range(n):
        if adj[i] and not visited[i]:
            print("NO EULERIAN TRAIL")
            return
            
    def reach(s):
        sn = [False] * n
        sn[s] = True
        st = [s]
        c = 0
        while st:
            u = st.pop()
            c += 1
            for w, e in adj[u]:
                if alive[e] and not sn[w]:
                    sn[w] = True
                    st.append(w)
        return c

    start = odd[0] if odd else src
    trail = [start]
    u = start
    while True:
        cands = [(w, e) for w, e in adj[u] if alive[e]]
        if not cands:
            break
        cands.sort()
        w, e = cands[0]
        if len(cands) > 1:
            base = reach(u)
            for nw, ne in cands:
                alive[ne] = False
                if reach(u) >= base:
                    alive[ne] = True
                    w = nw
                    e = ne
                    break
                alive[ne] = True
        alive[e] = False
        trail.append(w)
        u = w
        
    if any(alive):
        print("NO EULERIAN TRAIL")
        return
        
    print(" ".join(str(x) for x in trail))

if __name__ == "__main__":
    main()
