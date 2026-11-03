import math
import sys

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    S = float(tokens[0])
    K = float(tokens[1])
    T = float(tokens[2])
    r = float(tokens[3])
    sig = float(tokens[4])
    tp = tokens[5]
    
    d1 = (math.log(S / K) + (r + 0.5 * sig * sig) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    
    if tp == "call":
        price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
        delta = norm_cdf(d1)
        rho = K * T * math.exp(-r * T) * norm_cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        delta = norm_cdf(d1) - 1.0
        rho = -K * T * math.exp(-r * T) * norm_cdf(-d2)
        
    gamma = norm_pdf(d1) / (S * sig * math.sqrt(T))
    vega = S * norm_pdf(d1) * math.sqrt(T)
    term1 = -(S * norm_pdf(d1) * sig) / (2.0 * math.sqrt(T))
    if tp == "call":
        term1 -= r * K * math.exp(-r * T) * norm_cdf(d2)
    else:
        term1 += r * K * math.exp(-r * T) * norm_cdf(-d2)
    theta = term1
    
    sys.stdout.write(f"{price:.4f}\n{delta:.4f}\n{gamma:.4f}\n{vega:.4f}\n{theta:.4f}\n{rho:.4f}\n")

if __name__ == "__main__":
    main()
