import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    M = int(tokens[0])
    lam = float(tokens[1])
    r = [float(tokens[2 + i]) for i in range(M)]
    
    mu = sum(r) / M
    var = sum((x - mu) ** 2 for x in r) / (M - 1)
    
    v = var
    for x in r:
        v = lam * v + (1.0 - lam) * x * x
    ewma = v
    
    bom, ba, bb = 0.0, 0.0, 0.0
    bll = -1e300
    bgf = var
    
    r_sq = [x * x for x in r]
    
    for ai in range(1, 31):
        a = ai * 0.01
        for bi in range(60, 96):
            b = bi * 0.01
            if a + b >= 1.0:
                continue
            om = var * (1.0 - a - b)
            vv = var
            ll = 0.0
            for r2 in r_sq:
                ll += -0.5 * (math.log(vv) + r2 / vv)
                vv = om + a * r2 + b * vv
            if ll > bll:
                bll = ll
                bom = om
                ba = a
                bb = b
                bgf = vv
                
    sys.stdout.write(f"EWMA: {ewma:.6f}\n")
    sys.stdout.write(f"GARCH: {bom:.6f} {ba:.6f} {bb:.6f} {bll:.6f}\n")
    sys.stdout.write(f"GFILTER: {bgf:.6f}\n")

if __name__ == "__main__":
    main()
