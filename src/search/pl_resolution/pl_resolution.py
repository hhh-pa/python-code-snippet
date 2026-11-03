import sys

def norm(c):
    return sorted(set(c))

def is_taut(c):
    s = set(c)
    for x in s:
        if -x in s:
            return True
    return False

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
        clause_set = set()
        for _ in range(C):
            k = int(next(it))
            c = norm([int(next(it)) for _ in range(k)])
            if not is_taut(c):
                tc = tuple(c)
                if tc not in clause_set:
                    clause_set.add(tc)
                    clauses.append(c)
                    
        q = int(next(it))
        nq = (-q,)
        if nq not in clause_set:
            clause_set.add(nq)
            clauses.append([-q])
            
        entailed = False
        for _ in range(500):
            if entailed:
                break
            added = []
            added_set = set()
            n = len(clauses)
            for i in range(n):
                ci = clauses[i]
                for j in range(i + 1, n):
                    cj = clauses[j]
                    for l1 in ci:
                        if -l1 in cj:
                            # resolve on l1 and -l1
                            r = [x for x in ci if x != l1] + [x for x in cj if x != -l1]
                            r = norm(r)
                            if not r:
                                entailed = True
                                break
                            if is_taut(r):
                                continue
                            tr = tuple(r)
                            if tr not in clause_set and tr not in added_set:
                                added_set.add(tr)
                                added.append(r)
                    if entailed:
                        break
                if entailed:
                    break
                    
            if not added:
                break
            for c in added:
                clause_set.add(tuple(c))
                clauses.append(c)
            if len(clauses) > 4000:
                break
                
        if entailed:
            out.append("RESOLUTION ENTAILED")
        else:
            out.append("RESOLUTION NOT-ENTAILED")
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
