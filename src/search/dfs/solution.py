import sys

sys.setrecursionlimit(200000)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return
        
    grid = [[int(next(it)) for _ in range(m)] for _ in range(n)]
    
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    def measure_region(r, c):
        stack = [(r, c)]
        grid[r][c] = -1
        size = 0
        while stack:
            cr, cc = stack.pop()
            size += 1
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
                    grid[nr][nc] = -1
                    stack.append((nr, nc))
        return size

    max_region = -1
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 1:
                size = measure_region(r, c)
                if size > max_region:
                    max_region = size
                    
    print(max_region)

if __name__ == "__main__":
    main()
