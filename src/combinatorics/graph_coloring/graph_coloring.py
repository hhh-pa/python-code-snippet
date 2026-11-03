import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    n = int(tokens[1])
    m = int(tokens[2])
    
    adj = [[] for _ in range(n)]
    deg = [0] * n
    idx = 3
    for _ in range(m):
        u = int(tokens[idx])
        v = int(tokens[idx+1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
        
    order = list(range(n))
    if mode == "W":
        order.sort(key=lambda x: (-deg[x], x))
        
    color = [-1] * n
    for u in order:
        used = set()
        for w in adj[u]:
            cw = color[w]
            if cw >= 0:
                used.add(cw)
        c = 0
        while c in used:
            c += 1
        color[u] = c
        
    nc = max(color) + 1 if n > 0 else 0
    sys.stdout.write(f"{nc}\n")
    sys.stdout.write(" ".join(map(str, color)) + "\n")

if __name__ == "__main__":
    main()
