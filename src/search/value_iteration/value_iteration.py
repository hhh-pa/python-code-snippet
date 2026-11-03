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
        g = gn / gd
        K = int(next(it))
        
        U = [0.0] * S
        for _ in range(K):
            U2 = [0.0] * S
            for s in range(S):
                best = -1e300
                for a in range(A):
                    v = 0.0
                    for s2, p, r in tr[s][a]:
                        v += p * (r + g * U[s2])
                    if v > best:
                        best = v
                U2[s] = best
            U = U2
            
        pol = [0] * S
        for s in range(S):
            best = -1e300
            for a in range(A):
                v = 0.0
                for s2, p, r in tr[s][a]:
                    v += p * (r + g * U[s2])
                if v > best:
                    best = v
                    pol[s] = a
                    
        out.append("VI")
        out.append(" ".join(f"{U[s]:.6f}" for s in range(S)))
        out.append(" ".join(str(pol[s]) for s in range(S)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
