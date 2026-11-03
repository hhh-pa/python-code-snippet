import sys

sys.setrecursionlimit(200000)

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
        V = int(next(it))
        C = int(next(it))
        clauses = []
        for _ in range(C):
            k = int(next(it))
            clauses.append([int(next(it)) for _ in range(k)])
            
        def dpll(asn):
            while True:
                changed = False
                for c in clauses:
                    un = 0
                    ulit = 0
                    sat = False
                    for l in c:
                        x = abs(l) - 1
                        ax = asn[x]
                        if ax == -1:
                            un += 1
                            ulit = l
                        elif (ax == 1) == (l > 0):
                            sat = True
                            break
                    if sat:
                        continue
                    if un == 0:
                        return False
                    if un == 1:
                        x = abs(ulit) - 1
                        val = 1 if ulit > 0 else 0
                        if asn[x] == -1:
                            asn[x] = val
                            changed = True
                        elif asn[x] != val:
                            return False
                            
                pos = [False] * V
                neg = [False] * V
                for c in clauses:
                    sat = False
                    for l in c:
                        x = abs(l) - 1
                        ax = asn[x]
                        if ax != -1 and (ax == 1) == (l > 0):
                            sat = True
                            break
                    if sat:
                        continue
                    for l in c:
                        x = abs(l) - 1
                        if asn[x] == -1:
                            if l > 0:
                                pos[x] = True
                            else:
                                neg[x] = True
                for x in range(V):
                    if asn[x] == -1:
                        if pos[x] and not neg[x]:
                            asn[x] = 1
                            changed = True
                        elif neg[x] and not pos[x]:
                            asn[x] = 0
                            changed = True
                            
                if not changed:
                    break
                    
                for c in clauses:
                    sat = False
                    un = 0
                    for l in c:
                        x = abs(l) - 1
                        ax = asn[x]
                        if ax == -1:
                            un += 1
                        elif (ax == 1) == (l > 0):
                            sat = True
                            break
                    if not sat and un == 0:
                        return False

            for c in clauses:
                sat = False
                un = 0
                for l in c:
                    x = abs(l) - 1
                    ax = asn[x]
                    if ax == -1:
                        un += 1
                    elif (ax == 1) == (l > 0):
                        sat = True
                        break
                if not sat and un == 0:
                    return False
                    
            br = -1
            for x in range(V):
                if asn[x] == -1:
                    br = x
                    break
            if br < 0:
                return True
                
            a2 = list(asn)
            a2[br] = 1
            if dpll(a2):
                asn[:] = a2
                return True
                
            a3 = list(asn)
            a3[br] = 0
            if dpll(a3):
                asn[:] = a3
                return True
                
            return False

        asn = [-1] * V
        sat = dpll(asn)
        if not sat:
            out.append("DPLL UNSAT")
        else:
            row = ["DPLL SAT"]
            for x in asn:
                row.append("0" if x == -1 else str(x))
            out.append(" ".join(row))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
