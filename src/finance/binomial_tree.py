import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    S = float(tokens[0])
    K = float(tokens[1])
    T = float(tokens[2])
    r = float(tokens[3])
    sig = float(tokens[4])
    N = int(tokens[5])
    tp = tokens[6]
    style = tokens[7]
    
    dt = T / N
    u = math.exp(sig * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    p = (math.exp(r * dt) - d) / (u - d)
    p = max(0.0, min(1.0, p))
    
    vals = [0.0] * (N + 1)
    for j in range(N + 1):
        ST = S * (u**j) * (d ** (N - j))
        if tp == "call":
            vals[j] = max(ST - K, 0.0)
        else:
            vals[j] = max(K - ST, 0.0)
            
    for step in range(N - 1, -1, -1):
        for j in range(step + 1):
            hold = disc * (p * vals[j + 1] + (1 - p) * vals[j])
            if style == "american":
                ST = S * (u**j) * (d ** (step - j))
                intr = max(ST - K, 0.0) if tp == "call" else max(K - ST, 0.0)
                vals[j] = max(hold, intr)
            else:
                vals[j] = hold
                
    sys.stdout.write(f"{vals[0]:.4f}\n")

if __name__ == "__main__":
    main()
