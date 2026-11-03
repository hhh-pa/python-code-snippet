import sys
import math

def sn(x):
    if abs(x) < 5e-7:
        return 0.0
    return x

def norm_sq(c):
    return c.real * c.real + c.imag * c.imag

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    L = int(tokens[0])
    lambda_val = float(tokens[1])
    theta0 = float(tokens[2])
    n0 = float(tokens[3])
    ns = float(tokens[4])
    
    nn = [0.0] * L
    dd = [0.0] * L
    idx = 5
    for j in range(L):
        nn[j] = float(tokens[idx])
        dd[j] = float(tokens[idx+1])
        idx += 2
        
    PI = math.pi
    s0 = n0 * math.sin(theta0 * PI / 180.0)
    
    for pol in range(2):
        M11 = 1.0 + 0j
        M12 = 0j
        M21 = 0j
        M22 = 1.0 + 0j
        
        for j in range(L):
            st = s0 / nn[j]
            if st > 1.0:
                st = 1.0
            if st < -1.0:
                st = -1.0
            ct = math.sqrt(max(0.0, 1.0 - st * st))
            eta = nn[j] * ct if pol == 0 else nn[j] / ct
            delta = 2.0 * PI * nn[j] * dd[j] * ct / lambda_val
            c = math.cos(delta)
            s = math.sin(delta)
            iu = 1j
            N11 = complex(c, 0)
            N12 = iu * s / eta
            N21 = iu * eta * s
            N22 = complex(c, 0)
            O11 = M11 * N11 + M12 * N21
            O12 = M11 * N12 + M12 * N22
            O21 = M21 * N11 + M22 * N21
            O22 = M21 * N12 + M22 * N22
            M11 = O11
            M12 = O12
            M21 = O21
            M22 = O22
            
        st0 = math.sin(theta0 * PI / 180.0)
        ct0 = math.cos(theta0 * PI / 180.0)
        sts = s0 / ns
        if sts > 1.0:
            sts = 1.0
        if sts < -1.0:
            sts = -1.0
        cts = math.sqrt(max(0.0, 1.0 - sts * sts))
        e0 = n0 * ct0 if pol == 0 else n0 / ct0
        es = ns * cts if pol == 0 else ns / cts
        den = e0 * M11 + e0 * es * M12 + M21 + es * M22
        r = (e0 * M11 + e0 * es * M12 - M21 - es * M22) / den
        t = 2.0 * e0 / den
        R = norm_sq(r)
        T = (es / e0) * norm_sq(t)
        prefix = "S: " if pol == 0 else "P: "
        sys.stdout.write(f"{prefix}r {sn(r.real):.6f} {sn(r.imag):.6f} R {sn(R):.6f} T {sn(T):.6f}\n")

if __name__ == "__main__":
    main()
