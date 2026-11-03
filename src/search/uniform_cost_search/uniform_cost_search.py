import sys
import heapq

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
        g = int(next(it))
        
        adj = [[] for _ in range(N)]
        for _ in range(M):
            u = int(next(it))
            v = int(next(it))
            w = int(next(it))
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        for i in range(N):
            adj[i].sort()
            
        # Uniform-cost search
        dist = [INF] * N
        par = [-1] * N
        dist[s] = 0
        pq = [(0, s)]
        while pq:
            d, v = heapq.heappop(pq)
            if d != dist[v]:
                continue
            if v == g:
                break
            for to, w in adj[v]:
                nd = d + w
                if nd < dist[to]:
                    dist[to] = nd
                    par[to] = v
                    heapq.heappush(pq, (nd, to))
                    
        if dist[g] >= INF:
            out.append("UCS -1")
        else:
            path = []
            curr = g
            while curr != -1:
                path.append(curr)
                curr = par[curr]
            path.reverse()
            out.append(f"UCS {dist[g]} " + " ".join(map(str, path)))
            
        # Bidirectional Dijkstra
        ds = [INF] * N
        dg = [INF] * N
        ps = [-1] * N
        pg = [-1] * N
        vs = [False] * N
        vg = [False] * N
        ds[s] = 0
        dg[g] = 0
        vs[s] = True
        vg[g] = True
        
        qs = [(0, s)]
        qg = [(0, g)]
        best = INF
        meet = -1
        
        turn = 0
        while True:
            while qs and qs[0][0] != ds[qs[0][1]]:
                heapq.heappop(qs)
            while qg and qg[0][0] != dg[qg[0][1]]:
                heapq.heappop(qg)
            if not qs and not qg:
                break
            ts = qs[0][0] if qs else INF
            tg = qg[0][0] if qg else INF
            if best < INF and ts + tg >= best:
                break
                
            if turn % 2 == 0:
                if not qs:
                    turn += 1
                    continue
                d, v = heapq.heappop(qs)
                if d != ds[v]:
                    turn += 1
                    continue
                vs[v] = True
                if vg[v] and ds[v] + dg[v] < best:
                    best = ds[v] + dg[v]
                    meet = v
                for to, w in adj[v]:
                    nd = d + w
                    if nd < ds[to]:
                        ds[to] = nd
                        ps[to] = v
                        vs[to] = True
                        heapq.heappush(qs, (nd, to))
                        if vg[to] and nd + dg[to] < best:
                            best = nd + dg[to]
                            meet = to
            else:
                if not qg:
                    turn += 1
                    continue
                d, v = heapq.heappop(qg)
                if d != dg[v]:
                    turn += 1
                    continue
                vg[v] = True
                if vs[v] and ds[v] + dg[v] < best:
                    best = ds[v] + dg[v]
                    meet = v
                for to, w in adj[v]:
                    nd = d + w
                    if nd < dg[to]:
                        dg[to] = nd
                        pg[to] = v
                        vg[to] = True
                        heapq.heappush(qg, (nd, to))
                        if vs[to] and ds[to] + nd < best:
                            best = ds[to] + nd
                            meet = to
            turn += 1
            
        if meet < 0:
            out.append("BIDIR -1")
        else:
            left = []
            curr = meet
            while curr != -1:
                left.append(curr)
                curr = ps[curr]
            left.reverse()
            
            right = []
            curr = pg[meet]
            while curr != -1:
                right.append(curr)
                curr = pg[curr]
                
            bidir_path = left + right
            out.append(f"BIDIR {best} " + " ".join(map(str, bidir_path)))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
