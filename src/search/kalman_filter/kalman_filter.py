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
        Tl = int(next(it))
        qn = float(next(it))
        qd = float(next(it))
        rn = float(next(it))
        rd = float(next(it))
        q = qn / qd
        r = rn / rd
        
        x0n = float(next(it))
        x0d = float(next(it))
        p0n = float(next(it))
        p0d = float(next(it))
        x = x0n / x0d
        P = p0n / p0d
        
        zs = []
        for _ in range(Tl):
            n = float(next(it))
            d = float(next(it))
            zs.append(n / d)
            
        out.append("KALMAN")
        for k in range(Tl):
            P += q
            K = P / (P + r)
            x = x + K * (zs[k] - x)
            P = (1.0 - K) * P
            out.append(f"{x:.6f} {P:.6f}")
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
