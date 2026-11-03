import sys

sys.setrecursionlimit(200000)

INF = 1000000000

class Succ:
    __slots__ = ('f', 'to', 'w')
    def __init__(self, f, to, w):
        self.f = f
        self.to = to
        self.w = w

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
        
        def rbfs(v, g, f_limit):
            if v == goal:
                return -1
            succs = []
            for to, w in adj[v]:
                if onpath[to]:
                    continue
                succs.append(Succ(w + g + hval[to], to, w))
            if not succs:
                return INF
            fv = g + hval[v]
            for succ in succs:
                if succ.f < fv:
                    succ.f = fv
            while True:
                succs.sort(key=lambda s: (s.f, s.to))
                best = succs[0].f
                if best >= INF or best > f_limit:
                    return best
                alt = succs[1].f if len(succs) > 1 else INF
                to = succs[0].to
                w = succs[0].w
                lim = min(f_limit, alt)
                onpath[to] = True
                path.append(to)
                r = rbfs(to, g + w, lim)
                if r < 0:
                    return -1
                path.pop()
                onpath[to] = False
                succs[0].f = r

        dist = -1
        final_path = []
        if s == goal:
            dist = 0
            final_path = [s]
        else:
            r = rbfs(s, 0, INF)
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
                
        if dist < 0:
            out.append("RBFS -1")
        else:
            row = [f"RBFS {dist}"]
            for v in final_path:
                row.append(str(v))
            out.append(" ".join(row))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
