import sys

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

def attacking(b):
    n = len(b)
    c = 0
    for i in range(n):
        bi = b[i]
        for j in range(i + 1, n):
            bj = b[j]
            if bi == bj:
                c += 1
            elif abs(bi - bj) == j - i:
                c += 1
    return c

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
        k = int(next(it))
        seed = int(next(it)) & MASK64
        
        rng = LCG(seed)
        beam = []
        for _ in range(k):
            b = [rng.next_int(N) for _ in range(N)]
            beam.append(b)
            
        best_cost = 1 << 30
        best_board = list(beam[0])
        for b in beam:
            c = attacking(b)
            if c < best_cost:
                best_cost = c
                best_board = list(b)
                
        if best_cost != 0:
            for _ in range(100):
                succs = []
                for b in beam:
                    for r in range(N):
                        br = b[r]
                        for c2 in range(N):
                            if c2 == br:
                                continue
                            nb = list(b)
                            nb[r] = c2
                            succs.append((attacking(nb), nb))
                succs.sort(key=lambda x: (x[0], x[1]))
                new_beam = []
                for cost_val, nb in succs:
                    if not any(nb == ex for ex in new_beam):
                        new_beam.append(nb)
                        if len(new_beam) >= k:
                            break
                beam = new_beam
                for b in beam:
                    c = attacking(b)
                    if c < best_cost:
                        best_cost = c
                        best_board = list(b)
                if best_cost == 0:
                    break
                    
        out.append(" ".join(map(str, best_board)))
        out.append(str(best_cost))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
