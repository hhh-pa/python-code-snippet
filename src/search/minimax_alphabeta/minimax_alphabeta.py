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
        D = int(next(it))
        n = 1 << D
        leaves = [int(next(it)) for _ in range(n)]
        
        full_cnt = 0
        def mm_full(idx, depth, ismax):
            nonlocal full_cnt
            if depth == 0:
                full_cnt += 1
                return leaves[idx]
            a = mm_full(idx * 2, depth - 1, not ismax)
            b = mm_full(idx * 2 + 1, depth - 1, not ismax)
            return max(a, b) if ismax else min(a, b)
            
        ab_cnt = 0
        def mm_ab(idx, depth, ismax, alpha, beta):
            nonlocal ab_cnt
            if depth == 0:
                ab_cnt += 1
                return leaves[idx]
            if ismax:
                v = -2000000000
                r = mm_ab(idx * 2, depth - 1, False, alpha, beta)
                if r > v:
                    v = r
                if v > alpha:
                    alpha = v
                if alpha >= beta:
                    return v
                r = mm_ab(idx * 2 + 1, depth - 1, False, alpha, beta)
                if r > v:
                    v = r
                return v
            else:
                v = 2000000000
                r = mm_ab(idx * 2, depth - 1, True, alpha, beta)
                if r < v:
                    v = r
                if v < beta:
                    beta = v
                if alpha >= beta:
                    return v
                r = mm_ab(idx * 2 + 1, depth - 1, True, alpha, beta)
                if r < v:
                    v = r
                return v
                
        v1 = mm_full(0, D, True)
        mm_ab(0, D, True, -2000000000, 2000000000)
        out.append(f"MINIMAX {v1} FULL {full_cnt} AB {ab_cnt}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
