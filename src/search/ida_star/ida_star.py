import sys

sys.setrecursionlimit(200000)

INF = 1000000000

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        N = int(next(it))
        M = int(next(it))
        s = int(next(it))
        goal = int(next(it))
        
        adj = [[] for _ in range(N)]
        for _ in range(M):
            u = int(next(it))
            v = int(next(it))
            w = int(next(it))
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        for i in range(N):
            adj[i].sort()
            
        hval = [int(next(it)) for _ in range(N)]
        
        path = [s]
        onpath = [False] * N
        onpath[s] = True
        
        def dfs(v, g, bound):
            f = g + hval[v]
            if f > bound:
                return f
            if v == goal:
                return -1
            best = INF
            for to, w in adj[v]:
                if onpath[to]:
                    continue
                onpath[to] = True
                path.append(to)
                r = dfs(to, g + w, bound)
                if r < 0:
                    return -1
                path.pop()
                onpath[to] = False
                if r < best:
                    best = r
            return best
            
        dist = -1
        final_path = []
        if s == goal:
            dist = 0
            final_path = [s]
        else:
            bound = hval[s]
            for _ in range(100000):
                r = dfs(s, 0, bound)
                if r < 0:
                    g2 = 0
                    for i in range(1, len(path)):
                        x, y = path[i - 1], path[i]
                        for to, w in adj[x]:
                            if to == y:
                                g2 += w
                                break
                    dist = g2
                    final_path = list(path)
                    break
                if r >= INF:
                    break
                bound = r
                
        if dist < 0:
            out.append("IDA -1")
        else:
            row = [f"IDA {dist}"]
            for v in final_path:
                row.append(str(v))
            out.append(" ".join(row))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
