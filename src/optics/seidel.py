import sys
import math

def sn(x):
    if abs(x) < 5e-7:
        return 0.0
    return x

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    S = int(tokens[0])
    R = [0.0] * S
    th = [0.0] * S
    nd = [0.0] * S
    dn = [0.0] * S
    idx = 1
    for j in range(S):
        R[j] = float(tokens[idx])
        th[j] = float(tokens[idx+1])
        nd[j] = float(tokens[idx+2])
        dn[j] = float(tokens[idx+3])
        idx += 4
        
    h = float(tokens[idx])
    u = float(tokens[idx+1])
    hb = float(tokens[idx+2])
    ub = float(tokens[idx+3])
    
    H = ub * h - u * hb
    n = 1.0
    d = 0.0
    S1 = 0.0
    S2 = 0.0
    S3 = 0.0
    S4 = 0.0
    S5 = 0.0
    C1 = 0.0
    C2 = 0.0
    
    for j in range(S):
        c = 0.0 if R[j] == 0 else 1.0 / R[j]
        np = nd[j]
        dp = dn[j]
        up = (n * u - h * c * (np - n)) / np
        ubp = (n * ub - hb * c * (np - n)) / np
        A = n * (h * c + u)
        Ab = n * (hb * c + ub)
        dun = up / np - u / n
        dinv = 1.0 / np - 1.0 / n
        ddn = dp / np - d / n
        S1 += -A * A * h * dun
        S2 += -A * Ab * h * dun
        S3 += -Ab * Ab * h * dun
        S4 += -H * H * c * dinv
        if abs(A) > 1e-12:
            S5 += -(Ab / A) * (Ab * Ab * h * dun + H * H * c * dinv)
        C1 += h * A * ddn
        C2 += h * Ab * ddn
        h = h + up * th[j]
        u = up
        hb = hb + ubp * th[j]
        ub = ubp
        n = np
        d = dp
        
    sys.stdout.write(f"SEIDEL: {sn(S1):.6f} {sn(S2):.6f} {sn(S3):.6f} {sn(S4):.6f} {sn(S5):.6f}\n")
    sys.stdout.write(f"CHROM: {sn(C1):.6f} {sn(C2):.6f}\n")

if __name__ == "__main__":
    main()
