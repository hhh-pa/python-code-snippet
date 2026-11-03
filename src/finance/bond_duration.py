import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    ytm = float(tokens[0])
    m = int(tokens[1])
    kp = []
    cf = []
    idx = 2
    for _ in range(m):
        kp.append(int(tokens[idx]))
        cf.append(float(tokens[idx + 1]))
        idx += 2
        
    yp = ytm / 2.0
    P = 0.0
    for k, c in zip(kp, cf):
        P += c * ((1.0 + yp) ** (-k))
        
    dper = 0.0
    for k, c in zip(kp, cf):
        dper += k * c * ((1.0 + yp) ** (-k))
    dper /= P
    
    cper = 0.0
    for k, c in zip(kp, cf):
        cper += k * (k + 1) * c * ((1.0 + yp) ** (-k))
    cper /= (P * (1.0 + yp) * (1.0 + yp))
    
    mac = dper / 2.0
    mod = mac / (1.0 + yp)
    conv = cper / 4.0
    
    nk = int(tokens[idx])
    idx += 1
    keys = [int(tokens[idx + i]) for i in range(nk)]
    idx += nk
    
    krd = [0.0] * nk
    for j in range(nk):
        pu = 0.0
        pd = 0.0
        for k, c in zip(kp, cf):
            ru = yp + 0.0001 if k == keys[j] else yp
            pu += c * ((1.0 + ru) ** (-k))
            rd = yp - 0.0001 if k == keys[j] else yp
            pd += c * ((1.0 + rd) ** (-k))
        krd[j] = -(pu - pd) / (2.0 * P * 0.0001) / 2.0
        
    kl = int(tokens[idx])
    al = float(tokens[idx + 1])
    
    pl = al * ((1.0 + yp) ** (-kl))
    dl = float(kl)
    cl = float(kl * (kl + 1)) / ((1.0 + yp) * (1.0 + yp))
    
    imm = (abs(P - pl) / pl < 1e-6 and abs(dper - dl) < 1e-4 and cper > cl + 1e-9)
    
    sys.stdout.write(f"PRICE: {P:.6f}\n")
    sys.stdout.write(f"MAC: {mac:.6f}\n")
    sys.stdout.write(f"MOD: {mod:.6f}\n")
    sys.stdout.write(f"CONV: {conv:.6f}\n")
    krd_str = " ".join(f"{x:.6f}" for x in krd)
    sys.stdout.write(f"KRD: {krd_str}\n" if nk > 0 else "KRD:\n")
    sys.stdout.write(f"IMMUNIZED: {'YES' if imm else 'NO'}\n")

if __name__ == "__main__":
    main()
