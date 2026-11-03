import sys
import math

def sn(x):
    if abs(x) < 5e-7:
        return 0.0
    return x

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    N = int(tokens[0])
    mode = int(tokens[1])
    
    idx = 2
    A = [float(tokens[idx + j]) for j in range(N)]
    idx += N
    
    lam = 1.0
    z = 1.0
    dx = 1.0
    if mode == 1:
        lam = float(tokens[idx])
        z = float(tokens[idx+1])
        dx = float(tokens[idx+2])
        idx += 3
        
    PI = math.pi
    re = [0.0] * N
    im = [0.0] * N
    
    for j in range(N):
        if mode == 0:
            re[j] = A[j]
            im[j] = 0.0
        else:
            x = (j - N / 2.0) * dx
            ph = PI * x * x / (lam * z)
            re[j] = A[j] * math.cos(ph)
            im[j] = A[j] * math.sin(ph)
            
    # Bit-reversal permutation
    kk = 0
    for i in range(1, N):
        b = N >> 1
        while kk & b:
            kk &= ~b
            b >>= 1
        kk |= b
        if i < kk:
            re[i], re[kk] = re[kk], re[i]
            im[i], im[kk] = im[kk], im[i]
            
    m = 2
    while m <= N:
        ang = -2.0 * PI / m
        wr = math.cos(ang)
        wi = math.sin(ang)
        for k in range(0, N, m):
            cr = 1.0
            ci = 0.0
            for j in range(m // 2):
                tr = cr * re[k + j + m // 2] - ci * im[k + j + m // 2]
                ti = cr * im[k + j + m // 2] + ci * re[k + j + m // 2]
                re[k + j + m // 2] = re[k + j] - tr
                im[k + j + m // 2] = im[k + j] - ti
                re[k + j] += tr
                im[k + j] += ti
                nr = cr * wr - ci * wi
                ci = cr * wi + ci * wr
                cr = nr
        m *= 2
        
    mx = 0.0
    I = [0.0] * N
    for k in range(N):
        I[k] = re[k] * re[k] + im[k] * im[k]
        if I[k] > mx:
            mx = I[k]
            
    res = ["I:"]
    for k in range(N):
        val = sn(I[k] / mx) if mx > 0 else 0.0
        res.append(f"{val:.6f}")
    sys.stdout.write(" ".join(res) + "\n")

if __name__ == "__main__":
    main()
