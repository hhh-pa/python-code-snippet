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
    
    S = int(tokens[0])
    zv = [0.0] * S
    RR = [0.0] * S
    na = [0.0] * S
    idx = 1
    for j in range(S):
        zv[j] = float(tokens[idx])
        RR[j] = float(tokens[idx+1])
        na[j] = float(tokens[idx+2])
        idx += 3
        
    M = int(tokens[idx])
    idx += 1
    
    for m in range(M):
        ox = float(tokens[idx])
        oy = float(tokens[idx+1])
        oz = float(tokens[idx+2])
        dx = float(tokens[idx+3])
        dy = float(tokens[idx+4])
        dz = float(tokens[idx+5])
        idx += 6
        
        dl = math.sqrt(dx * dx + dy * dy + dz * dz)
        dx /= dl
        dy /= dl
        dz /= dl
        
        n1 = 1.0
        opl = 0.0
        ok = True
        hx = [0.0] * S
        hy = [0.0] * S
        
        for j in range(S):
            t = -1.0
            if RR[j] == 0:
                if dz != 0:
                    t = (zv[j] - oz) / dz
            else:
                cx = 0.0
                cy = 0.0
                cz = zv[j] + RR[j]
                ocx = ox - cx
                ocy = oy - cy
                ocz = oz - cz
                b = dx * ocx + dy * ocy + dz * ocz
                c = ocx * ocx + ocy * ocy + ocz * ocz - RR[j] * RR[j]
                disc = b * b - c
                if disc >= 0:
                    sq = math.sqrt(disc)
                    t1 = -b - sq
                    t2 = -b + sq
                    if t1 > 1e-9:
                        t = t1
                    elif t2 > 1e-9:
                        t = t2
            if t < 1e-9:
                ok = False
                break
            opl += n1 * t
            px = ox + dx * t
            py = oy + dy * t
            pz = oz + dz * t
            hx[j] = px
            hy[j] = py
            
            if RR[j] == 0:
                nx = 0.0
                ny = 0.0
                nz = 1.0
            else:
                ar = abs(RR[j])
                nx = px / ar
                ny = py / ar
                nz = (pz - (zv[j] + RR[j])) / ar
                nl = math.sqrt(nx * nx + ny * ny + nz * nz)
                nx /= nl
                ny /= nl
                nz /= nl
                
            if dx * nx + dy * ny + dz * nz > 0:
                nx = -nx
                ny = -ny
                nz = -nz
                
            eta = n1 / na[j]
            c1 = -(dx * nx + dy * ny + dz * nz)
            s2t = eta * eta * (1.0 - c1 * c1)
            if s2t > 1.0:
                ok = False
                break
            c2 = math.sqrt(max(0.0, 1.0 - s2t))
            k = eta * c1 - c2
            dx = eta * dx + k * nx
            dy = eta * dy + k * ny
            dz = eta * dz + k * nz
            ox = px + dx * 1e-9
            oy = py + dy * 1e-9
            oz = pz + dz * 1e-9
            n1 = na[j]
            
        if not ok:
            sys.stdout.write(f"RAY {m} MISS\n")
            continue
            
        hits = " ".join(f"{sn(hx[j]):.6f} {sn(hy[j]):.6f}" for j in range(S))
        sys.stdout.write(f"RAY {m} HIT: {hits}\n")
        sys.stdout.write(f"RAY {m} DIR: {sn(dx):.6f} {sn(dy):.6f} {sn(dz):.6f}\n")
        sys.stdout.write(f"RAY {m} OPL: {sn(opl):.6f}\n")

if __name__ == "__main__":
    main()
