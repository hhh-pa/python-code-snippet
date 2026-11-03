import sys

def r2score(y, p):
    n = len(y)
    mu = sum(y) / n
    sse = sum((y[i] - p[i]) ** 2 for i in range(n))
    sst = sum((y[i] - mu) ** 2 for i in range(n))
    if sst == 0:
        return 1.0 if sse == 0 else 0.0
    return 1.0 - sse / sst

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    p = int(tokens[1])
    idx = 2
    X = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            X[i][j] = float(tokens[idx])
            idx += 1
    y = [float(tokens[idx + i]) for i in range(n)]
    idx += n
    w = [float(tokens[idx + j]) for j in range(p)]
    idx += p
    
    mu = sum(y) / n
    tot = sum((v - mu) ** 2 for v in y)
    
    mdi = [0.0] * p
    mda = [0.0] * p
    sfi = [0.0] * p
    
    # MDI
    for j in range(p):
        order = list(range(n))
        order.sort(key=lambda i: (X[i][j], i))
        best = 0.0
        for s in range(1, n):
            if X[order[s]][j] == X[order[s - 1]][j]:
                continue
            nl = s
            nr = n - s
            sum_l = sum(y[order[t]] for t in range(s))
            sum_r = sum(y[order[t]] for t in range(s, n))
            ml = sum_l / nl
            mr = sum_r / nr
            sl = sum((y[order[t]] - ml) ** 2 for t in range(s))
            sr = sum((y[order[t]] - mr) ** 2 for t in range(s, n))
            gain = tot - sl - sr
            if gain > best:
                best = gain
        mdi[j] = best
        
    # MDA
    base = [sum(X[i][j] * w[j] for j in range(p)) for i in range(n)]
    r2b = r2score(y, base)
    for j in range(p):
        pr = [0.0] * n
        for i in range(n):
            s = 0.0
            for k in range(p):
                val = X[(i + 1) % n][k] if k == j else X[i][k]
                s += val * w[k]
            pr[i] = s
        mda[j] = r2b - r2score(y, pr)
        
    # SFI
    for j in range(p):
        mx = sum(X[i][j] for i in range(n)) / n
        cov = sum((X[i][j] - mx) * (y[i] - mu) for i in range(n))
        vv = sum((X[i][j] - mx) ** 2 for i in range(n))
        slope = cov / vv if vv != 0 else 0.0
        icept = mu - slope * mx
        pr = [icept + slope * X[i][j] for i in range(n)]
        sfi[j] = r2score(y, pr)
        
    mdi_str = " ".join(f"{v:.6f}" for v in mdi)
    mda_str = " ".join(f"{v:.6f}" for v in mda)
    sfi_str = " ".join(f"{v:.6f}" for v in sfi)
    
    sys.stdout.write(f"MDI: {mdi_str}\n")
    sys.stdout.write(f"MDA: {mda_str}\n")
    sys.stdout.write(f"SFI: {sfi_str}\n")

if __name__ == "__main__":
    main()
