import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    M = int(tokens[0])
    H = int(tokens[1])
    up = float(tokens[2])
    dn = float(tokens[3])
    idx = 4
    px = [float(tokens[idx + i]) for i in range(M)]
    idx += M
    E = int(tokens[idx])
    idx += 1
    
    lab = [0] * E
    meta = [0] * E
    for j in range(E):
        t0 = int(tokens[idx])
        side = int(tokens[idx + 1])
        idx += 2
        L = 0
        end_t = min(M, t0 + H + 1)
        for t in range(t0 + 1, end_t):
            rr = px[t] - px[t0]
            if rr >= up - 1e-12:
                L = 1
                break
            if rr <= -dn + 1e-12:
                L = -1
                break
        lab[j] = L
        meta[j] = 1 if (L != 0 and side == L) else 0
        
    labels_str = " ".join(str(x) for x in lab)
    meta_str = " ".join(str(x) for x in meta)
    sys.stdout.write(f"LABELS: {labels_str}\n" if E > 0 else "LABELS:\n")
    sys.stdout.write(f"META: {meta_str}\n" if E > 0 else "META:\n")

if __name__ == "__main__":
    main()
