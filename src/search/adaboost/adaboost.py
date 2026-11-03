import sys
import math

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
        F = int(next(it))
        R = int(next(it))
        
        X = []
        Y = []
        for _ in range(N):
            row = [int(next(it)) for _ in range(F)]
            y = int(next(it))
            X.append(row)
            Y.append(y)
            
        w = [1.0 / N] * N
        ef = []
        et = []
        ep = []
        ea = []
        
        for _ in range(R):
            bf, bt, bpol = 0, 0, 0
            be = 1e300
            for f in range(F):
                vals = sorted(set(X[i][f] for i in range(N)))
                for th in vals:
                    for pol in (0, 1):
                        e = 0.0
                        for i in range(N):
                            h = 1 if (X[i][f] >= th) == (pol == 1) else 0
                            if h != Y[i]:
                                e += w[i]
                        if e < be - 1e-12:
                            be = e
                            bf = f
                            bt = th
                            bpol = pol
            if be >= 0.5:
                break
            alpha = 10.0 if be <= 0 else 0.5 * math.log((1.0 - be) / be)
            tot = 0.0
            for i in range(N):
                h = 1.0 if (X[i][bf] >= bt) == (bpol == 1) else -1.0
                yy = 1.0 if Y[i] == 1 else -1.0
                w[i] *= math.exp(-alpha * yy * h)
                tot += w[i]
            for i in range(N):
                w[i] /= tot
            ef.append(bf)
            et.append(bt)
            ep.append(bpol)
            ea.append(alpha)
            if be <= 0:
                break
                
        P = []
        err = 0
        for i in range(N):
            s = 0.0
            for k in range(len(ea)):
                h = 1.0 if (X[i][ef[k]] >= et[k]) == (ep[k] == 1) else -1.0
                s += ea[k] * h
            pred = 1 if s >= 0 else 0
            P.append(pred)
            if pred != Y[i]:
                err += 1
                
        out.append(f"ADA {len(ea)} {err}")
        out.append(" ".join(map(str, P)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
