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
        V = int(next(it))
        C = int(next(it))
        MF = int(next(it))
        pn = int(next(it))
        pd = int(next(it))
        seed = int(next(it)) & MASK64
        
        clauses = []
        for _ in range(C):
            k = int(next(it))
            clauses.append([int(next(it)) for _ in range(k)])
            
        rng = LCG(seed)
        asn = [rng.next_int(2) for _ in range(V)]
        
        def sat_lit(l):
            v = abs(l) - 1
            return (asn[v] == 1) == (l > 0)
            
        def sat_cls(c):
            return any(sat_lit(l) for l in c)
            
        def all_sat():
            return all(sat_cls(c) for c in clauses)
            
        solved = all_sat()
        for _ in range(MF):
            if solved:
                break
            unsat = [i for i in range(C) if not sat_cls(clauses[i])]
            ci = unsat[rng.next_int(len(unsat))]
            cl = clauses[ci]
            
            if (rng.next() % pd) < pn:
                pick = abs(cl[rng.next_int(len(cl))]) - 1
            else:
                best = 1000000000
                pick = 0
                for l in cl:
                    v = abs(l) - 1
                    brk = 0
                    asn[v] ^= 1
                    for c2 in clauses:
                        if sat_cls(c2):
                            continue
                        asn[v] ^= 1
                        was = sat_cls(c2)
                        asn[v] ^= 1
                        if was:
                            brk += 1
                    asn[v] ^= 1
                    if brk < best:
                        best = brk
                        pick = v
            asn[pick] ^= 1
            if all_sat():
                solved = True
                
        status = "SAT" if solved else "UNKNOWN"
        row = [f"WALKSAT {status}"]
        for v in range(V):
            row.append(str(asn[v]))
        out.append(" ".join(row))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
