import sys
import heapq

def manhattan(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        pr = int(next(it))
        pc = int(next(it))
        fr = int(next(it))
        fc = int(next(it))
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return
        
    grid = [next(it) for _ in range(n)]
    
    inf = 1 << 30
    dist = [[inf] * m for _ in range(n)]
    parent = [[None] * m for _ in range(n)]
    
    dist[pr][pc] = 0
    # heap elements: (cost, r, c, g)
    h = [(manhattan(pr, pc, fr, fc), pr, pc, 0)]
    
    dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    
    while h:
        cost, r, c, g = heapq.heappop(h)
        if g != dist[r][c]:
            continue
        if r == fr and c == fc:
            break
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '%':
                new_g = g + 1
                if new_g < dist[nr][nc]:
                    dist[nr][nc] = new_g
                    parent[nr][nc] = (r, c)
                    new_cost = g + manhattan(nr, nc, fr, fc)
                    heapq.heappush(h, (new_cost, nr, nc, new_g))
                    
    if dist[fr][fc] == inf:
        return
        
    path = []
    cur = (fr, fc)
    path.append(cur)
    while cur != (pr, pc):
        cur = parent[cur[0]][cur[1]]
        path.append(cur)
        
    path.reverse()
    print(len(path) - 1)
    for r, c in path:
        print(f"{r} {c}")

if __name__ == "__main__":
    main()
