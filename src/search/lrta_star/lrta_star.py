import sys

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
        R = int(next(it))
        C = int(next(it))
        grid = [[int(next(it)) for _ in range(C)] for _ in range(R)]
        sr = int(next(it))
        sc = int(next(it))
        gr = int(next(it))
        gc = int(next(it))
        
        def h_man(r, c):
            return abs(r - gr) + abs(c - gc)
            
        H = {}
        def get_h(r, c):
            return H.get((r, c), h_man(r, c))
            
        dr = [-1, 1, 0, 0]
        dc = [0, 0, -1, 1]
        
        cr, cc = sr, sc
        steps = 0
        path = [(cr, cc)]
        MAX_STEPS = 10000
        
        while not (cr == gr and cc == gc) and steps < MAX_STEPS:
            nbrs = []
            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                    nbrs.append((nr, nc))
            if not nbrs:
                break
                
            min_h = min(1 + get_h(nr, nc) for nr, nc in nbrs)
            H[(cr, cc)] = min_h
            
            best = nbrs[0]
            best_h = 1 + get_h(best[0], best[1])
            for nb in nbrs[1:]:
                hv = 1 + get_h(nb[0], nb[1])
                if hv < best_h or (hv == best_h and nb < best):
                    best_h = hv
                    best = nb
                    
            cr, cc = best
            path.append((cr, cc))
            steps += 1
            
        out.append(str(steps))
        path_str = " ".join(f"{r} {c}" for r, c in path)
        out.append(path_str)
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
