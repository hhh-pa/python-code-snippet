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

    def next_double(self):
        return float(self.next() >> 11) * 1.1102230246251565e-16

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
        S = int(next(it))
        O = int(next(it))
        N = int(next(it))
        Tl = int(next(it))
        seed = int(next(it)) & MASK64
        
        tr = []
        for _ in range(S):
            row = []
            for _ in range(S):
                n = float(next(it))
                d = float(next(it))
                row.append(n / d)
            tr.append(row)
            
        se = []
        for _ in range(S):
            row = []
            for _ in range(O):
                n = float(next(it))
                d = float(next(it))
                row.append(n / d)
            se.append(row)
            
        obs = [int(next(it)) for _ in range(Tl)]
        
        rng = LCG(seed)
        parts = [rng.next_int(S) for _ in range(N)]
        
        out.append("PF")
        for k in range(Tl):
            ob = obs[k]
            for i in range(N):
                u = rng.next_double()
                c = 0.0
                ns = S - 1
                row_tr = tr[parts[i]]
                for j in range(S):
                    c += row_tr[j]
                    if u < c:
                        ns = j
                        break
                parts[i] = ns
                
            w = [se[parts[i]][ob] for i in range(N)]
            tot = sum(w)
            
            np_parts = [0] * N
            if tot == 0.0:
                for i in range(N):
                    np_parts[i] = rng.next_int(S)
            else:
                cw = [0.0] * (N + 1)
                inv_tot = 1.0 / tot
                for i in range(N):
                    cw[i + 1] = cw[i] + w[i] * inv_tot
                for i in range(N):
                    u = rng.next_double()
                    pick = N - 1
                    for j in range(N):
                        if u < cw[j + 1]:
                            pick = j
                            break
                    np_parts[i] = parts[pick]
            parts = np_parts
            
            hist = [0] * S
            for x in parts:
                hist[x] += 1
            out.append(" ".join(map(str, hist)))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
