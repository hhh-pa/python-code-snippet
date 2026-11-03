import math
import sys

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    rets = [float(tokens[1 + i]) for i in range(n)]
    rf = float(tokens[1 + n])
    sr_benchmark = float(tokens[2 + n]) if len(tokens) > 2 + n else 0.0
    
    mu = sum(rets) / n
    excess_mu = mu - rf
    var = sum((x - mu) ** 2 for x in rets) / (n - 1)
    sd = math.sqrt(var)
    sr = excess_mu / sd * math.sqrt(252.0) if sd != 0 else 0.0
    
    m2 = sum((x - mu) ** 2 for x in rets) / n
    m3 = sum((x - mu) ** 3 for x in rets) / n
    m4 = sum((x - mu) ** 4 for x in rets) / n
    
    skew = m3 / (m2 ** 1.5) if m2 != 0 else 0.0
    kurt = m4 / (m2 * m2) if m2 != 0 else 0.0
    
    numer = (sr - sr_benchmark) * math.sqrt(n - 1)
    denom2 = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if denom2 < 0:
        denom2 = 1.0
    denom = math.sqrt(denom2)
    psr = norm_cdf(numer / denom)
    
    sys.stdout.write(f"{sr:.4f}\n{psr:.4f}\n")

if __name__ == "__main__":
    main()
