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
        N = int(next(it))
        parents = [[] for _ in range(N)]
        children = [[] for _ in range(N)]
        cpt = [[] for _ in range(N)]
        
        for v in range(N):
            k = int(next(it))
            for _ in range(k):
                p = int(next(it))
                parents[v].append(p)
                children[p].append(v)
            rows = 1 << k
            cpt_v = [0.0] * rows
            for r in range(rows):
                nn = float(next(it))
                dd = float(next(it))
                cpt_v[r] = nn / dd
            cpt[v] = cpt_v
            
        q = int(next(it))
        ne = int(next(it))
        evid = [-1] * N
        for _ in range(ne):
            e = int(next(it))
            vv = int(next(it))
            evid[e] = vv
            
        S = int(next(it))
        seed = int(next(it)) & MASK64
        
        def prow(v, asn):
            k = len(parents[v])
            row = 0
            for j in range(k):
                row |= (asn[parents[v][j]] << (k - 1 - j))
            return cpt[v][row]
            
        # Rejection sampling
        rng = LCG(seed)
        acc, qt = 0, 0
        asn = [0] * N
        for _ in range(S):
            for v in range(N):
                asn[v] = 1 if rng.next_double() < prow(v, asn) else 0
            ok = True
            for v in range(N):
                if evid[v] >= 0 and asn[v] != evid[v]:
                    ok = False
                    break
            if ok:
                acc += 1
                if asn[q] == 1:
                    qt += 1
        out.append(f"REJECT {acc} {qt}")
        
        # Likelihood weighting
        rng = LCG(seed)
        wt, wq = 0.0, 0.0
        asn = [0] * N
        for _ in range(S):
            w = 1.0
            for v in range(N):
                if evid[v] >= 0:
                    asn[v] = evid[v]
                    pr = prow(v, asn)
                    w *= pr if evid[v] == 1 else (1.0 - pr)
                else:
                    asn[v] = 1 if rng.next_double() < prow(v, asn) else 0
            wt += w
            if asn[q] == 1:
                wq += w
        est = 0.0 if wt == 0 else wq / wt
        out.append(f"LIKELIHOOD {est:.6f}")
        
        # Gibbs sampling
        rng = LCG(seed)
        asn = [evid[v] if evid[v] >= 0 else rng.next_int(2) for v in range(N)]
        
        def gibbs_prob(v, asn):
            asn[v] = 1
            pt = prow(v, asn)
            for c in children[v]:
                p = prow(c, asn)
                pt *= p if asn[c] == 1 else (1.0 - p)
            asn[v] = 0
            pv = 1.0 - prow(v, asn)
            for c in children[v]:
                p = prow(c, asn)
                pv *= p if asn[c] == 1 else (1.0 - p)
            if pt + pv == 0:
                return 1.0 if asn[v] == 1 else 0.0
            return pt / (pt + pv)
            
        for _ in range(10):
            for v in range(N):
                if evid[v] >= 0:
                    continue
                asn[v] = 1 if rng.next_double() < gibbs_prob(v, asn) else 0
                
        qt = 0
        for _ in range(S):
            for v in range(N):
                if evid[v] >= 0:
                    continue
                asn[v] = 1 if rng.next_double() < gibbs_prob(v, asn) else 0
            if asn[q] == 1:
                qt += 1
        out.append(f"GIBBS {qt} {S}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
