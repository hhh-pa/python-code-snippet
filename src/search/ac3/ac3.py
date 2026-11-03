import sys
from collections import deque

def holds(a, b, op):
    if op == 0:
        return a != b
    if op == 1:
        return a == b
    if op == 2:
        return a < b
    return a > b

def flipop(op):
    if op == 2:
        return 3
    if op == 3:
        return 2
    return op

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
        N = int(next(it))
        dom = []
        for _ in range(N):
            sz = int(next(it))
            vals = [int(next(it)) for _ in range(sz)]
            vals.sort()
            dom.append(vals)
        
        C = int(next(it))
        nbr = [[] for _ in range(N)]
        for _ in range(C):
            u = int(next(it))
            v = int(next(it))
            op = int(next(it))
            nbr[u].append((v, op))
            nbr[v].append((u, flipop(op)))
            
        q = deque()
        for i in range(N):
            for v, op in nbr[i]:
                q.append((i, v, op))
                
        ok = True
        while q and ok:
            ai, aj, aop = q.popleft()
            nd = []
            ch = False
            for x in dom[ai]:
                sup = any(holds(x, y, aop) for y in dom[aj])
                if sup:
                    nd.append(x)
                else:
                    ch = True
            if ch:
                dom[ai] = nd
                if not nd:
                    ok = False
                    break
                for v, op in nbr[ai]:
                    if v != aj:
                        q.append((v, ai, op))
                        
        if not ok:
            out.append("AC3 INCONSISTENT")
        else:
            out.append("AC3")
            for i in range(N):
                out.append(" ".join(map(str, dom[i])))
                
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
