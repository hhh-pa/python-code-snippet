import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    d = float(tokens[0])
    L = int(tokens[1])
    M = int(tokens[2])
    x = [float(tokens[3 + i]) for i in range(M)]
    
    w = [0.0] * L
    w[0] = 1.0
    for k in range(1, L):
        w[k] = -w[k - 1] * (d - k + 1) / k
        
    w_str = " ".join(f"{v:.6f}" for v in w)
    sys.stdout.write(f"W: {w_str}\n")
    
    y = []
    for t in range(L - 1, M):
        s = sum(w[k] * x[t - k] for k in range(L))
        y.append(s)
        
    y_str = " ".join(f"{v:.6f}" for v in y)
    sys.stdout.write(f"Y: {y_str}\n" if y else "Y:\n")

if __name__ == "__main__":
    main()
