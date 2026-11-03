import math
import sys

def erf7(x):
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    s = -1.0 if x < 0 else 1.0
    ax = abs(x)
    t = 1.0 / (1.0 + p * ax)
    poly = ((((a5 * t + a4) * t + a3) * t + a2) * t + a1)
    return s * (1.0 - poly * t * math.exp(-ax * ax))

def ncdf(x):
    return 0.5 * (1.0 + erf7(x / math.sqrt(2.0)))

def phiinv(p):
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
    elif p <= 0.97575:
        q = p - 0.5
        r = q * q
        return (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q / (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / (((((d1 * q + d2) * q + d3) * q + d4) * q + 1.0))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    E = float(tokens[0])
    sE = float(tokens[1])
    D = float(tokens[2])
    rr = float(tokens[3])
    T = float(tokens[4])
    
    sA = sE * E / (E + D)
    A = E + D * math.exp(-rr * T)
    for _ in range(100):
        for _ in range(50):
            d1 = (math.log(A / D) + (rr + 0.5 * sA * sA) * T) / (sA * math.sqrt(T))
            d2 = d1 - sA * math.sqrt(T)
            C = A * ncdf(d1) - D * math.exp(-rr * T) * ncdf(d2)
            delta = ncdf(d1)
            A = A - (C - E) / delta
        d1 = (math.log(A / D) + (rr + 0.5 * sA * sA) * T) / (sA * math.sqrt(T))
        sA = sE * E / (ncdf(d1) * A)
        
    DD = (math.log(A / D) + (rr - 0.5 * sA * sA) * T) / (sA * math.sqrt(T))
    PD = ncdf(-DD)
    
    p = float(tokens[5])
    rho = float(tokens[6])
    att = float(tokens[7])
    det = float(tokens[8])
    
    gx = [0.3429013272237046, 1.036610829789514, 1.756683649299882, 2.53273167423279, 3.436159118837738]
    gw = [0.6108626337353258, 0.2401386110823147, 0.03387439445548106, 0.001343645746781232, 7.64043285523262e-06]
    
    pinv = phiinv(p)
    sqr = math.sqrt(rho)
    sq1 = math.sqrt(1.0 - rho)
    acc = 0.0
    for i in range(5):
        for s in (-1, 1):
            z = s * math.sqrt(2.0) * gx[i]
            P = ncdf((pinv - sqr * z) / sq1)
            L = (P - att) / (det - att)
            if L < 0:
                L = 0.0
            if L > 1:
                L = 1.0
            acc += gw[i] * L
            
    el = acc / math.sqrt(math.pi)
    
    sys.stdout.write(f"MERTON: {A:.6f} {sA:.6f} {DD:.6f} {PD:.6f}\n")
    sys.stdout.write(f"VASICEK: {el:.6f}\n")

if __name__ == "__main__":
    main()
