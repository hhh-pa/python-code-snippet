import sys
import math

def sn(x):
    if abs(x) < 5e-7:
        return 0.0
    return x

def mmul(A, B):
    R = [0j] * 4
    for i in range(2):
        for j in range(2):
            s = 0j
            for k in range(2):
                s += A[i * 2 + k] * B[k * 2 + j]
            R[i * 2 + j] = s
    return R

def m4mul(A, B):
    R = [0j] * 16
    for i in range(4):
        for j in range(4):
            s = 0j
            for k in range(4):
                s += A[i * 4 + k] * B[k * 4 + j]
            R[i * 4 + j] = s
    return R

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    E = int(tokens[0])
    idx = 1
    PI = math.pi
    J = [1.0 + 0j, 0j, 0j, 1.0 + 0j]
    
    for _ in range(E):
        kind = tokens[idx]
        idx += 1
        T = [0j] * 4
        if kind == "P":
            th = float(tokens[idx])
            idx += 1
            a = th * PI / 180.0
            c = math.cos(a)
            s = math.sin(a)
            T[0] = complex(c * c, 0)
            T[1] = complex(c * s, 0)
            T[2] = complex(c * s, 0)
            T[3] = complex(s * s, 0)
        elif kind == "W":
            dl = float(tokens[idx])
            th = float(tokens[idx+1])
            idx += 2
            d = dl * PI / 180.0
            a = th * PI / 180.0
            c = math.cos(a)
            s = math.sin(a)
            R = [complex(c, 0), complex(s, 0), complex(-s, 0), complex(c, 0)]
            RI = [complex(c, 0), complex(-s, 0), complex(s, 0), complex(c, 0)]
            D = [complex(math.cos(d / 2), math.sin(d / 2)), 0j, 0j, complex(math.cos(d / 2), -math.sin(d / 2))]
            T = mmul(RI, mmul(D, R))
        else: # Rotator
            ph = float(tokens[idx])
            idx += 1
            a = ph * PI / 180.0
            c = math.cos(a)
            s = math.sin(a)
            T[0] = complex(c, 0)
            T[1] = complex(-s, 0)
            T[2] = complex(s, 0)
            T[3] = complex(c, 0)
        J = mmul(T, J)
        
    exr = float(tokens[idx])
    exi = float(tokens[idx+1])
    eyr = float(tokens[idx+2])
    eyi = float(tokens[idx+3])
    idx += 4
    
    S = [float(tokens[idx + i]) for i in range(4)]
    idx += 4
    
    Ein = [complex(exr, exi), complex(eyr, eyi)]
    ox = J[0] * Ein[0] + J[1] * Ein[1]
    oy = J[2] * Ein[0] + J[3] * Ein[1]
    
    K = [0j] * 16
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    z = J[k * 2 + l]
                    K[(i * 2 + k) * 4 + (j * 2 + l)] = J[i * 2 + j] * complex(z.real, -z.imag)
                    
    A = [0j] * 16
    ad = [1, 0, 0, 1, 1, 0, 0, -1, 0, 1, 1, 0, 0, 0, 0, 0]
    for i in range(16):
        A[i] = complex(ad[i], 0)
    A[13] = 1j
    A[14] = -1j
    
    AI = [0j] * 16
    AI[0] = complex(0.5, 0)
    AI[1] = complex(0.5, 0)
    AI[6] = complex(0.5, 0)
    AI[7] = complex(0, -0.5)
    AI[10] = complex(0.5, 0)
    AI[11] = complex(0, 0.5)
    AI[12] = complex(0.5, 0)
    AI[13] = complex(-0.5, 0)
    
    M = m4mul(A, m4mul(K, AI))
    
    O = [0.0] * 4
    for i in range(4):
        for j in range(4):
            O[i] += M[i * 4 + j].real * S[j]
            
    jones_str = "JONES:" + "".join(f" {sn(J[i].real):.6f} {sn(J[i].imag):.6f}" for i in range(4))
    mueller_str = "MUELLER:" + "".join(f" {sn(M[i].real):.6f}" for i in range(16))
    out_j_str = f"OUT_J: {sn(ox.real):.6f} {sn(ox.imag):.6f} {sn(oy.real):.6f} {sn(oy.imag):.6f}"
    out_s_str = "OUT_S:" + "".join(f" {sn(O[i]):.6f}" for i in range(4))
    
    sys.stdout.write(f"{jones_str}\n{mueller_str}\n{out_j_str}\n{out_s_str}\n")

if __name__ == "__main__":
    main()
