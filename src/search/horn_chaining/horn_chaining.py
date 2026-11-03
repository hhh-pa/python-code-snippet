import sys
from collections import deque

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
        R = int(next(it))
        
        prem = []
        concl = []
        byprem = [[] for _ in range(V)]
        for i in range(R):
            k = int(next(it))
            p_list = [int(next(it)) for _ in range(k)]
            c = int(next(it))
            prem.append(p_list)
            concl.append(c)
            for x in p_list:
                byprem[x].append(i)
                
        q = int(next(it))
        
        # Forward chaining
        count = [len(prem[i]) for i in range(R)]
        inferred = [False] * V
        ag = deque()
        for i in range(R):
            if count[i] == 0 and not inferred[concl[i]]:
                inferred[concl[i]] = True
                ag.append(concl[i])
                
        fc = False
        while ag and not fc:
            p = ag.popleft()
            if p == q:
                fc = True
                break
            for ri in byprem[p]:
                count[ri] -= 1
                if count[ri] == 0:
                    c = concl[ri]
                    if not inferred[c]:
                        inferred[c] = True
                        ag.append(c)
                        
        # Backward chaining
        byconcl = [[] for _ in range(V)]
        for i in range(R):
            byconcl[concl[i]].append(i)
            
        isfact = [False] * V
        for i in range(R):
            if not prem[i]:
                isfact[concl[i]] = True
                
        proved = [False] * V
        visiting = [False] * V
        
        def prove(g):
            if proved[g]:
                return True
            if visiting[g]:
                return False
            if isfact[g]:
                proved[g] = True
                return True
            visiting[g] = True
            for ri in byconcl[g]:
                all_ok = True
                for pr in prem[ri]:
                    if not prove(pr):
                        all_ok = False
                        break
                if all_ok:
                    proved[g] = True
                    visiting[g] = False
                    return True
            visiting[g] = False
            return False

        bc = prove(q)
        fcs = "YES" if fc else "NO"
        bcs = "YES" if bc else "NO"
        out.append(f"HORN FC:{fcs} BC:{bcs}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
