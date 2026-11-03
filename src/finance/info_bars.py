import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    N = int(tokens[0])
    V = float(tokens[1])
    D = float(tokens[2])
    T = float(tokens[3])
    R = float(tokens[4])
    M = int(tokens[5])
    
    px = []
    vol = []
    idx = 6
    for _ in range(M):
        px.append(float(tokens[idx]))
        vol.append(float(tokens[idx + 1]))
        idx += 2
        
    nt = M // N
    tickc = px[nt * N - 1] if nt > 0 else px[0]
    
    nv = 0
    acc = 0.0
    volc = px[0]
    for k in range(M):
        acc += vol[k]
        if acc >= V - 1e-12:
            nv += 1
            acc = 0.0
            volc = px[k]
            
    nd = 0
    acc = 0.0
    dollc = px[0]
    for k in range(M):
        acc += px[k] * vol[k]
        if acc >= D - 1e-12:
            nd += 1
            acc = 0.0
            dollc = px[k]
            
    ntib = 0
    cum = 0.0
    tibc = px[0]
    prev = 1
    for k in range(1, M):
        if px[k] > px[k - 1]:
            b = 1
        elif px[k] < px[k - 1]:
            b = -1
        else:
            b = prev
        prev = b
        cum += b
        if abs(cum) >= T - 1e-12:
            ntib += 1
            cum = 0.0
            tibc = px[k]
            
    nvr = 0
    cumv = 0.0
    vrc = px[0]
    prev = 1
    for k in range(1, M):
        if px[k] > px[k - 1]:
            b = 1
        elif px[k] < px[k - 1]:
            b = -1
        else:
            b = prev
        prev = b
        cumv += b * vol[k]
        if abs(cumv) >= R - 1e-12:
            nvr += 1
            cumv = 0.0
            vrc = px[k]
            
    sys.stdout.write(f"TICK: {nt} {tickc:.2f}\n")
    sys.stdout.write(f"VOLUME: {nv} {volc:.2f}\n")
    sys.stdout.write(f"DOLLAR: {nd} {dollc:.2f}\n")
    sys.stdout.write(f"TIB: {ntib} {tibc:.2f}\n")
    sys.stdout.write(f"VRUN: {nvr} {vrc:.2f}\n")

if __name__ == "__main__":
    main()
