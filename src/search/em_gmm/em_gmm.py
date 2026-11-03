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
        IT = int(next(it))
        x = []
        for _ in range(N):
            n = float(next(it))
            d = float(next(it))
            x.append(n / d)
            
        mn = min(x)
        mx = max(x)
        mean = sum(x) / N
        va = sum((v - mean) ** 2 for v in x) / N
        if va < 1e-6:
            va = 1e-6
            
        w0, w1 = 0.5, 0.5
        mu0, mu1 = mn, mx
        v0, v1 = va, va
        g0 = [0.0] * N
        g1 = [0.0] * N
        
        for _ in range(IT):
            sqrt_v0 = math.sqrt(v0)
            sqrt_v1 = math.sqrt(v1)
            for i in range(N):
                p0 = w0 * math.exp(-0.5 * (x[i] - mu0) * (x[i] - mu0) / v0) / sqrt_v0
                p1 = w1 * math.exp(-0.5 * (x[i] - mu1) * (x[i] - mu1) / v1) / sqrt_v1
                s = p0 + p1
                if s == 0.0:
                    g0[i] = 0.5
                    g1[i] = 0.5
                else:
                    g0[i] = p0 / s
                    g1[i] = p1 / s
                    
            n0 = sum(g0)
            n1 = sum(g1)
            w0 = n0 / N
            w1 = n1 / N
            mu0 = sum(g0[i] * x[i] for i in range(N)) / n0
            mu1 = sum(g1[i] * x[i] for i in range(N)) / n1
            v0 = sum(g0[i] * (x[i] - mu0) * (x[i] - mu0) for i in range(N)) / n0
            v1 = sum(g1[i] * (x[i] - mu1) * (x[i] - mu1) for i in range(N)) / n1
            if v0 < 1e-6:
                v0 = 1e-6
            if v1 < 1e-6:
                v1 = 1e-6
                
        if mu1 < mu0:
            w0, w1 = w1, w0
            mu0, mu1 = mu1, mu0
            v0, v1 = v1, v0
            for i in range(N):
                g0[i], g1[i] = g1[i], g0[i]
                
        out.append("EM")
        out.append(f"{w0:.6f} {mu0:.6f} {v0:.6f} {w1:.6f} {mu1:.6f} {v1:.6f}")
        preds = ["1" if g1[i] > g0[i] else "0" for i in range(N)]
        out.append(" ".join(preds))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
