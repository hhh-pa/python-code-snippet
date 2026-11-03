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
        A = int(next(it))
        
        tr = [[[] for _ in range(A)] for _ in range(S)]
        for s in range(S):
            for a in range(A):
                nt = int(next(it))
                transitions = []
                for _ in range(nt):
                    s2 = int(next(it))
                    n = float(next(it))
                    d = float(next(it))
                    r = float(next(it))
                    transitions.append((s2, n / d, r))
                tr[s][a] = transitions
                
        gn = float(next(it))
        gd = float(next(it))
        an = float(next(it))
        ad = float(next(it))
        en = float(next(it))
        ed = float(next(it))
        g = gn / gd
        al = an / ad
        eps = en / ed
        
        E = int(next(it))
        L = int(next(it))
        seed = int(next(it)) & MASK64
        
        def egreedy(rng, Q, s):
            u = rng.next_double()
            if u < eps:
                return rng.next_int(A)
            ba = 0
            bv = Q[s][0]
            for a in range(1, A):
                if Q[s][a] > bv:
                    bv = Q[s][a]
                    ba = a
            return ba

        def step(rng, s, a):
            u = rng.next_double()
            c = 0.0
            last_t = tr[s][a][-1]
            ns = last_t[0]
            rw = last_t[2]
            for s2, p, r in tr[s][a]:
                c += p
                if u < c:
                    ns = s2
                    rw = r
                    break
            return ns, rw

        # Q-learning
        rng = LCG(seed)
        Q = [[0.0] * A for _ in range(S)]
        for _ in range(E):
            s = 0
            for _ in range(L):
                a = egreedy(rng, Q, s)
                ns, rw = step(rng, s, a)
                mx = max(Q[ns])
                Q[s][a] += al * (rw + g * mx - Q[s][a])
                s = ns
                
        out.append("QLEARN")
        for s in range(S):
            out.append(" ".join(f"{Q[s][a]:.6f}" for a in range(A)))
        qp = ["QP"]
        for s in range(S):
            ba = 0
            for a in range(1, A):
                if Q[s][a] > Q[s][ba]:
                    ba = a
            qp.append(str(ba))
        out.append(" ".join(qp))
        
        # SARSA
        rng = LCG(seed)
        Q = [[0.0] * A for _ in range(S)]
        for _ in range(E):
            s = 0
            a = egreedy(rng, Q, 0)
            for _ in range(L):
                ns, rw = step(rng, s, a)
                na = egreedy(rng, Q, ns)
                Q[s][a] += al * (rw + g * Q[ns][na] - Q[s][a])
                s = ns
                a = na
                
        out.append("SARSA")
        for s in range(S):
            out.append(" ".join(f"{Q[s][a]:.6f}" for a in range(A)))
        sp = ["SP"]
        for s in range(S):
            ba = 0
            for a in range(1, A):
                if Q[s][a] > Q[s][ba]:
                    ba = a
            sp.append(str(ba))
        out.append(" ".join(sp))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
