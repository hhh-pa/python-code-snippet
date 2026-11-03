import sys
from collections import deque

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        Q_str = next(it)
    except StopIteration:
        return
    queries = int(Q_str)
    
    out = []
    for _ in range(queries):
        n = int(next(it))
        m = int(next(it))
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            adj[u].append(v)
            adj[v].append(u)
            
        start = int(next(it)) - 1
        dist = [-1] * n
        dist[start] = 0
        q = deque([start])
        while q:
            cur = q.popleft()
            nd = dist[cur] + 6
            for nxt in adj[cur]:
                if dist[nxt] == -1 or nd < dist[nxt]:
                    dist[nxt] = nd
                    q.append(nxt)
                    
        row = []
        for i in range(n):
            if i == start:
                continue
            row.append(str(dist[i]))
            if i != n - 1:
                row.append(" ")
        row.append("\n")
        out.append("".join(row))
        
    sys.stdout.write("".join(out))

if __name__ == "__main__":
    main()
