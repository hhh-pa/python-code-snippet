import sys
import math

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        R = int(next(it))
        C = int(next(it))
        
        u1 = [[0] * C for _ in range(R)]
        u2 = [[0] * C for _ in range(R)]
        for i in range(R):
            for j in range(C):
                u1[i][j] = int(next(it))
                u2[i][j] = int(next(it))
                
        rows = [True] * R
        cols = [True] * C
        changed = True
        while changed:
            changed = False
            nrows = list(rows)
            for i in range(R):
                if not rows[i]:
                    continue
                for k in range(R):
                    if k == i or not rows[k]:
                        continue
                    dom = True
                    for j in range(C):
                        if not cols[j]:
                            continue
                        if not (u1[k][j] > u1[i][j]):
                            dom = False
                            break
                    if dom:
                        nrows[i] = False
                        changed = True
                        break
            rows = nrows
            
            ncols = list(cols)
            for j in range(C):
                if not cols[j]:
                    continue
                for k in range(C):
                    if k == j or not cols[k]:
                        continue
                    dom = True
                    for i in range(R):
                        if not rows[i]:
                            continue
                        if not (u2[i][k] > u2[i][j]):
                            dom = False
                            break
                    if dom:
                        ncols[j] = False
                        changed = True
                        break
            cols = ncols
            
        rr = [i for i in range(R) if rows[i]]
        cc = [j for j in range(C) if cols[j]]
        
        pure = []
        for i in rr:
            for j in cc:
                b1 = True
                b2 = True
                for k in rr:
                    if u1[k][j] > u1[i][j]:
                        b1 = False
                        break
                for k in cc:
                    if u2[i][k] > u2[i][j]:
                        b2 = False
                        break
                if b1 and b2:
                    pure.append((i, j))
                    
        out.append(f"NASH {len(rr)} {len(cc)}")
        pure_row = [f"PURE {len(pure)}"]
        for i, j in pure:
            pure_row.append(f"{i}:{j}")
        out.append(" ".join(pure_row))
        
        if len(rr) == 2 and len(cc) == 2:
            a, b = rr[0], rr[1]
            c, d = cc[0], cc[1]
            pn = u2[b][d] - u2[b][c]
            pd = (u2[a][c] - u2[b][c]) - (u2[a][d] - u2[b][d])
            qn = u1[b][d] - u1[a][d]
            qd = (u1[a][c] - u1[a][d]) - (u1[b][c] - u1[b][d])
            ok = (pd != 0 and qd != 0)
            if ok:
                if pd < 0:
                    pn = -pn
                    pd = -pd
                if qd < 0:
                    qn = -qn
                    qd = -qd
                gp = math.gcd(pn, pd)
                gq = math.gcd(qn, qd)
                pn //= gp
                pd //= gp
                qn //= gq
                qd //= gq
                if not (0 < pn < pd and 0 < qn < qd):
                    ok = False
            if not ok:
                out.append("MIXED NONE")
            else:
                out.append(f"MIXED {pn}/{pd} {qn}/{qd}")
        else:
            out.append("MIXED NONE")
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
