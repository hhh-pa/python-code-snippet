import sys

def attacking(b):
    n = len(b)
    cnt = 0
    for i in range(n):
        bi = b[i]
        for j in range(i + 1, n):
            bj = b[j]
            if bi == bj:
                cnt += 1
            elif abs(bi - bj) == j - i:
                cnt += 1
    return cnt

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
        board = [int(next(it)) for _ in range(N)]
        
        while True:
            cur = attacking(board)
            if cur == 0:
                break
            best_val = cur
            best_row = -1
            best_col = -1
            for r in range(N):
                old = board[r]
                for c in range(N):
                    if c == old:
                        continue
                    board[r] = c
                    v = attacking(board)
                    if v < best_val:
                        best_val = v
                        best_row = r
                        best_col = c
                board[r] = old
                
            if best_row == -1:
                break
            board[best_row] = best_col
            
        out.append(" ".join(map(str, board)))
        out.append(str(attacking(board)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
