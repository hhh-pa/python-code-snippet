import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    v_count = int(next(it))
    e_count = int(next(it))
    
    edges = []
    adj = [[] for _ in range(v_count)]
    for _ in range(e_count):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))
        adj[u].append((v, w))
        
    INF = 10**18
    h = [0] * v_count
    for iteration in range(v_count):
        updated = False
        for u, v, w in edges:
            if h[u] + w < h[v]:
                h[v] = h[u] + w
                updated = True
        if not updated:
            break
        if iteration == v_count - 1:
            print("NEGATIVE CYCLE")
            return
            
    out = []
    for src in range(v_count):
        d = [INF] * v_count
        d[src] = 0
        pq = [(0, src)]
        while pq:
            cur_d, u = heapq.heappop(pq)
            if cur_d > d[u]:
                continue
            for v, w in adj[u]:
                rw = w + h[u] - h[v]
                if cur_d + rw < d[v]:
                    d[v] = cur_d + rw
                    heapq.heappush(pq, (d[v], v))
        row = []
        for v in range(v_count):
            if d[v] >= INF // 2:
                row.append("INF")
            else:
                real_dist = d[v] + h[v] - h[src]
                row.append(str(real_dist))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
