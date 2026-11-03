import math
import sys

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

def tlog(a, b):
    if b == 0:
        return 0.0
    return b * math.log(a)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    M = int(tokens[0])
    alpha = float(tokens[1])
    MCN = int(tokens[2])
    rets = [float(tokens[3 + i]) for i in range(M)]
    
    mu = sum(rets) / M
    vv = sum((x - mu) ** 2 for x in rets) / (M - 1)
    sd = math.sqrt(vv)
    z = phiinv(alpha)
    pvar = -(mu + sd * z)
    pes = sd * math.exp(-z * z / 2.0) / math.sqrt(2.0 * math.pi) / alpha - mu
    
    s = sorted(rets)
    idx = max(0, int(math.ceil(alpha * M)) - 1)
    hvar = -s[idx]
    hes = -sum(s[: idx + 1]) / (idx + 1)
    
    lcg = 42
    MASK = 0xFFFFFFFFFFFFFFFF
    sim = []
    while len(sim) < MCN:
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & MASK
        u1 = ((lcg >> 11) + 1) / 9007199254740992.0
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & MASK
        u2 = ((lcg >> 11) + 1) / 9007199254740992.0
        rad = math.sqrt(-2.0 * math.log(u1))
        sim.append(mu + sd * rad * math.cos(2.0 * math.pi * u2))
        if len(sim) < MCN:
            sim.append(mu + sd * rad * math.sin(2.0 * math.pi * u2))
            
    sim.sort()
    j = max(0, int(math.ceil(alpha * MCN)) - 1)
    mvar = -sim[j]
    mes = -sum(sim[: j + 1]) / (j + 1)
    
    hit = [1 if rets[i] < -hvar else 0 for i in range(M)]
    x = sum(hit)
    kup = -2.0 * (tlog(1.0 - alpha, M - x) + tlog(alpha, x)) + 2.0 * (tlog(1.0 - x / M, M - x) + tlog(x / M, x))
    
    n00, n01, n10, n11 = 0, 0, 0, 0
    for i in range(1, M):
        if hit[i - 1] == 0 and hit[i] == 0:
            n00 += 1
        elif hit[i - 1] == 0 and hit[i] == 1:
            n01 += 1
        elif hit[i - 1] == 1 and hit[i] == 0:
            n10 += 1
        else:
            n11 += 1
            
    pi0 = n01 / (n00 + n01) if n00 + n01 > 0 else 0.0
    pi1 = n11 / (n10 + n11) if n10 + n11 > 0 else 0.0
    pi = (n01 + n11) / (M - 1)
    chr_val = -2.0 * (tlog(1.0 - pi, n00 + n10) + tlog(pi, n01 + n11)) + 2.0 * (tlog(1.0 - pi0, n00) + tlog(pi0, n01) + tlog(1.0 - pi1, n10) + tlog(pi1, n11))
    
    sys.stdout.write(f"PVAR: {pvar:.6f} PES: {pes:.6f}\n")
    sys.stdout.write(f"HVAR: {hvar:.6f} HES: {hes:.6f}\n")
    sys.stdout.write(f"MVAR: {mvar:.6f} MES: {mes:.6f}\n")
    sys.stdout.write(f"KUPIEC: {kup:.6f}\n")
    sys.stdout.write(f"CHRIST: {chr_val:.6f}\n")

if __name__ == "__main__":
    main()
