import sys
import math

MASK64 = 0xFFFFFFFFFFFFFFFF
MULT = 6364136223846793005
ADD = 1442695040888963407

class LCG:
    def __init__(self, s):
        self.s = s & MASK64

    def next(self):
        self.s = (self.s * MULT + ADD) & MASK64
        return self.s

    def next_int(self, n):
        return int(self.next() % n)

    def next_double(self):
        return float(self.next() >> 11) * (1.0 / 9007199254740992.0)

def attacking_pairs(b):
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
        seed = int(next(it)) & MASK64
        
        temp = 100.0
        cooling = 0.99
        temp_min = 0.01
        max_steps = 5000
        
        rng = LCG(seed)
        cur_cost = attacking_pairs(board)
        best_cost = cur_cost
        best_board = list(board)
        steps = 0
        
        while temp > temp_min and steps < max_steps:
            r = rng.next_int(N)
            c = rng.next_int(N)
            if c == board[r]:
                c = (c + 1) % N
            old = board[r]
            board[r] = c
            new_cost = attacking_pairs(board)
            delta = new_cost - cur_cost
            if delta < 0 or rng.next_double() < math.exp(-delta / temp):
                cur_cost = new_cost
                if cur_cost < best_cost:
                    best_cost = cur_cost
                    best_board = list(board)
            else:
                board[r] = old
            temp *= cooling
            steps += 1
            
        out.append(" ".join(map(str, best_board)))
        out.append(str(best_cost))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
