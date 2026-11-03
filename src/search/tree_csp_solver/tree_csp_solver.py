import sys

def holds(a, b, op):
    if op == 0:
        return a != b
    if op == 1:
        return a == b
    if op == 2:
        return a < b
    return a > b

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
        par = [int(next(it)) for _ in range(N)]
        dom = []
        for _ in range(N):
            sz = int(next(it))
            vals = [int(next(it)) for _ in range(sz)]
            vals.sort()
            dom.append(vals)
            
        op = [-1] * N
        for i in range(N):
            if par[i] >= 0:
                op[i] = int(next(it))
                
        kids = [[] for _ in range(N)]
        root = 0
        for i in range(N):
            if par[i] < 0:
                root = i
            else:
                kids[par[i]].append(i)
                
        order = []
        st = [root]
        while st:
            v = st.pop()
            order.append(v)
            for k in kids[v]:
                st.append(k)
                
        ok = True
        for oi in range(len(order) - 1, -1, -1):
            v = order[oi]
            if par[v] < 0:
                continue
            pp = par[v]
            op_v = op[v]
            dom_v = dom[v]
            nd = []
            for x in dom[pp]:
                if any(holds(x, y, op_v) for y in dom_v):
                    nd.append(x)
            dom[pp] = nd
            if not nd:
                ok = False
                break
                
        asn = [-1] * N
        if ok:
            for oi in range(len(order)):
                v = order[oi]
                if par[v] < 0:
                    if not dom[v]:
                        ok = False
                        break
                    asn[v] = dom[v][0]
                else:
                    op_v = op[v]
                    p_val = asn[par[v]]
                    f = False
                    for y in dom[v]:
                        if holds(p_val, y, op_v):
                            asn[v] = y
                            f = True
                            break
                    if not f:
                        ok = False
                        break
                        
        if not ok:
            out.append("TREECSP INCONSISTENT")
        else:
            out.append("TREECSP " + " ".join(map(str, asn)))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
