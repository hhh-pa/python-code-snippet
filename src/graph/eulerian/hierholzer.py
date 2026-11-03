import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    
    adj = [[] for _ in range(n)]
    in_deg = [0] * n
    out_deg = [0] * n
    
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        out_deg[u] += 1
        in_deg[v] += 1
        
    for i in range(n):
        adj[i].sort(reverse=True)
        
    start_node = -1
    end_node = -1
    bad_nodes = 0
    
    for i in range(n):
        if out_deg[i] - in_deg[i] == 1:
            if start_node != -1:
                bad_nodes = 100
            start_node = i
        elif in_deg[i] - out_deg[i] == 1:
            if end_node != -1:
                bad_nodes = 100
            end_node = i
        elif in_deg[i] != out_deg[i]:
            bad_nodes = 100
            
    if bad_nodes == 0 and start_node == -1 and end_node == -1:
        is_circuit = True
        for i in range(n):
            if out_deg[i] > 0:
                start_node = i
                break
        if start_node == -1:
            start_node = 0
    elif bad_nodes == 0 and start_node != -1 and end_node != -1:
        is_circuit = False
    else:
        print("NO EULERIAN PATH")
        return
        
    st = [start_node]
    path = []
    
    while st:
        u = st[-1]
        if adj[u]:
            v = adj[u].pop()
            st.append(v)
        else:
            path.append(u)
            st.pop()
            
    path.reverse()
    
    if len(path) != m + 1:
        print("NO EULERIAN PATH")
        return
        
    if is_circuit:
        print("CIRCUIT")
    else:
        print("PATH")
        
    print(" ".join(str(x) for x in path))

if __name__ == "__main__":
    main()
