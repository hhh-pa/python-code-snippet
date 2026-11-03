import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    L = int(tokens[0])
    K = int(tokens[1])
    t0 = []
    t1 = []
    idx = 2
    Tmax = 0
    for _ in range(L):
        a = int(tokens[idx])
        b = int(tokens[idx + 1])
        t0.append(a)
        t1.append(b)
        if b > Tmax:
            Tmax = b
        idx += 2
        
    c = [0] * (Tmax + 1)
    for i in range(L):
        for t in range(t0[i], t1[i] + 1):
            c[t] += 1
            
    u = [0.0] * L
    for i in range(L):
        s = sum(1.0 / c[t] for t in range(t0[i], t1[i] + 1))
        u[i] = s / (t1[i] - t0[i] + 1)
        
    uniq_str = " ".join(f"{x:.6f}" for x in u)
    sys.stdout.write(f"UNIQ: {uniq_str}\n")
    
    lcg = 999
    MASK = 0xFFFFFFFFFFFFFFFF
    draws = []
    uu = list(u)
    for d in range(K):
        tot = sum(uu)
        pick = 0
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & MASK
        if tot <= 0:
            pick = ((lcg >> 11) + 1) % L
        else:
            rr = (((lcg >> 11) + 1) / 9007199254740992.0) * tot
            acc = 0.0
            pick = L - 1
            for i in range(L):
                acc += uu[i]
                if acc > rr:
                    pick = i
                    break
        draws.append(pick)
        for t in range(t0[pick], t1[pick] + 1):
            for j in range(L):
                if t0[j] <= t <= t1[j]:
                    uu[j] -= (1.0 / c[t]) / (t1[j] - t0[j] + 1)
                    if uu[j] < 0:
                        uu[j] = 0.0
                        
    boot_str = " ".join(str(x) for x in draws)
    sys.stdout.write(f"BOOT: {boot_str}\n")

if __name__ == "__main__":
    main()
