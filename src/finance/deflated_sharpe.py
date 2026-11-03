import math
import sys

def aerf(x):
    s = -1.0 if x < 0 else 1.0
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t) * math.exp(-x * x)
    return s * y

def Phi(x):
    return 0.5 * (1.0 + aerf(x / math.sqrt(2.0)))

def PhiInv(p):
    a1 = -3.969683028665376e+01
    a2 = 2.209460984245205e+02
    a3 = -2.759285104469687e+02
    a4 = 1.383577518672690e+02
    a5 = -3.066479806614716e+01
    a6 = 2.506628277459239e+00
    b1 = -5.447609879822406e+01
    b2 = 1.615858368580409e+02
    b3 = -1.556989798598866e+02
    b4 = 6.680131188771972e+01
    b5 = -1.328068155288572e+01
    c1 = -7.784894002430293e-03
    c2 = -3.223964580411365e-01
    c3 = -2.400758277161838e+00
    c4 = -2.549732539343734e+00
    c5 = 4.374664141464968e+00
    c6 = 2.938163982698783e+00
    d1 = 7.784695709041462e-03
    d2 = 3.224671290700398e-01
    d3 = 2.445134137142996e+00
    d4 = 3.754408661907416e+00
    if p < 0.02425:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / (((((d1 * q + d2) * q + d3) * q + d4) * q + 1.0))
    if p > 0.97575:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / (((((d1 * q + d2) * q + d3) * q + d4) * q + 1.0))
    q = p - 0.5
    r = q * q
    return (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q / (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1.0)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    N = int(tokens[0])
    K = int(tokens[1])
    bench = float(tokens[2])
    idx = 3
    r = [float(tokens[idx + i]) for i in range(N)]
    idx += N
    tr = [float(tokens[idx + i]) for i in range(K)]
    idx += K
    
    m = sum(r) / N
    v = 0.0
    m2 = 0.0
    m3 = 0.0
    m4 = 0.0
    for x in r:
        d = x - m
        d2 = d * d
        v += d2
        m2 += d2
        m3 += d2 * d
        m4 += d2 * d2
    v /= (N - 1)
    m2 /= N
    m3 /= N
    m4 /= N
    sd = math.sqrt(v)
    SR = m / sd * math.sqrt(252.0)
    g3 = m3 / (m2 ** 1.5)
    g4 = m4 / (m2 * m2)
    den = 1.0 - g3 * SR + (g4 - 1.0) / 4.0 * SR * SR
    if den <= 0:
        den = 1e-12
    sc = math.sqrt(N - 1) / math.sqrt(den)
    PSR = Phi((SR - bench) * sc)
    
    tm = sum(tr) / K
    V = 0.0
    if K > 1:
        V = sum((x - tm) ** 2 for x in tr) / (K - 1)
        
    SR0 = 0.0
    if K >= 2:
        g = 0.5772156649015329
        e = 2.718281828459045
        a1 = PhiInv(1.0 - 1.0 / K)
        a2 = PhiInv(1.0 - 1.0 / (K * e))
        SR0 = math.sqrt(V) * ((1.0 - g) * a1 + g * a2)
        
    DSR = Phi((SR - SR0) * sc)
    
    sys.stdout.write(f"SR: {SR + 0.0:.6f}\n")
    sys.stdout.write(f"SKEW: {g3 + 0.0:.6f} KURT: {g4 + 0.0:.6f}\n")
    sys.stdout.write(f"PSR: {PSR + 0.0:.6f}\n")
    sys.stdout.write(f"DSR: {DSR + 0.0:.6f} SR0: {SR0 + 0.0:.6f}\n")

if __name__ == "__main__":
    main()
