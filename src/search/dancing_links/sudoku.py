import sys

def box_id(r, c):
    return (r // 3) * 3 + (c // 3)

def solve(board, rows, cols, boxes):
    best_r = -1
    best_c = -1
    best_mask = 0
    best_count = 10
    
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                continue
            b = box_id(r, c)
            used = rows[r] | cols[c] | boxes[b]
            mask = 0
            count = 0
            for d in range(1, 10):
                bit = 1 << d
                if not (used & bit):
                    mask |= bit
                    count += 1
            if count == 0:
                return False
            if count < best_count:
                best_count = count
                best_r = r
                best_c = c
                best_mask = mask
                if count == 1:
                    break
        if best_count == 1:
            break
            
    if best_r == -1:
        return True
        
    b = box_id(best_r, best_c)
    for d in range(1, 10):
        bit = 1 << d
        if not (best_mask & bit):
            continue
        board[best_r][best_c] = d
        rows[best_r] |= bit
        cols[best_c] |= bit
        boxes[b] |= bit
        
        if solve(board, rows, cols, boxes):
            return True
            
        rows[best_r] &= ~bit
        cols[best_c] &= ~bit
        boxes[b] &= ~bit
        board[best_r][best_c] = 0
        
    return False

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
        board = [[0] * 9 for _ in range(9)]
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        
        for r in range(9):
            for c in range(9):
                v = int(next(it))
                board[r][c] = v
                if v != 0:
                    bit = 1 << v
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[box_id(r, c)] |= bit
                    
        solve(board, rows, cols, boxes)
        for r in range(9):
            out.append("".join(f"{board[r][c]} " for c in range(9)))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
