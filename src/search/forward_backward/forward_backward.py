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
        O = int(next(it))
        Tl = int(next(it))
        
        pi = []
        for _ in range(S):
            n = float(next(it))
            d = float(next(it))
            pi.append(n / d)
            
        A = []
        for _ in range(S):
            row = []
            for _ in range(S):
                n = float(next(it))
                d = float(next(it))
                row.append(n / d)
            A.append(row)
            
        B = []
        for _ in range(S):
            row = []
            for _ in range(O):
                n = float(next(it))
                d = float(next(it))
                row.append(n / d)
            B.append(row)
            
        obs = [int(next(it)) for _ in range(Tl)]
        
        al = [[0.0] * S for _ in range(Tl)]
        be = [[0.0] * S for _ in range(Tl)]
        
        for i in range(S):
            al[0][i] = pi[i] * B[i][obs[0]]
            
        for k in range(1, Tl):
            ob = obs[k]
            al_prev = al[k - 1]
            al_cur = al[k]
            for j in range(S):
                s = sum(al_prev[i] * A[i][j] for i in range(S))
                al_cur[j] = s * B[j][ob]
                
        for i in range(S):
            be[Tl - 1][i] = 1.0
            
        for k in range(Tl - 2, -1, -1):
            next_ob = obs[k + 1]
            be_next = be[k + 1]
            be_cur = be[k]
            # Precompute B[j][next_ob] * be_next[j]
            weight = [B[j][next_ob] * be_next[j] for j in range(S)]
            for i in range(S):
                be_cur[i] = sum(A[i][j] * weight[j] for j in range(S))
                
        out.append("FB")
        for k in range(Tl):
            al_k = al[k]
            be_k = be[k]
            tot = sum(al_k[i] * be_k[i] for i in range(S))
            row = []
            for i in range(S):
                g = 0.0 if tot == 0 else (al_k[i] * be_k[i] / tot)
                row.append(f"{g:.6f}")
            out.append(" ".join(row))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
