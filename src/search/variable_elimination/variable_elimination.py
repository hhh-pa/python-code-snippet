import sys
import math

def norm(p, q):
    if q < 0:
        p = -p
        q = -q
    g = math.gcd(p, q)
    if g == 0:
        g = 1
    return p // g, q // g

def mul(a, b):
    return norm(a[0] * b[0], a[1] * b[1])

def add(a, b):
    return norm(a[0] * b[1] + b[0] * a[1], a[1] * b[1])

class Factor:
    __slots__ = ('scope', 'tab')
    def __init__(self, scope, tab):
        self.scope = scope
        self.tab = tab

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
        parents = [[] for _ in range(N)]
        cpt = [[] for _ in range(N)]
        for v in range(N):
            k = int(next(it))
            parents[v] = [int(next(it)) for _ in range(k)]
            rows = 1 << k
            cpt_v = []
            for _ in range(rows):
                nn = int(next(it))
                dd = int(next(it))
                cpt_v.append(norm(nn, dd))
            cpt[v] = cpt_v
            
        q = int(next(it))
        ne = int(next(it))
        evid = [-1] * N
        for _ in range(ne):
            e = int(next(it))
            vv = int(next(it))
            evid[e] = vv
            
        facs = []
        for v in range(N):
            sc = sorted([v] + parents[v])
            sz = len(sc)
            ln = 1 << sz
            tab = [None] * ln
            k = len(parents[v])
            for i in range(ln):
                vv = 0
                for j in range(sz):
                    if sc[j] == v:
                        vv = (i >> (sz - 1 - j)) & 1
                row = 0
                for j in range(k):
                    pj = parents[v][j]
                    pos = sc.index(pj)
                    bit = (i >> (sz - 1 - pos)) & 1
                    row |= (bit << (k - 1 - j))
                pr = cpt[v][row]
                if vv == 1:
                    tab[i] = pr
                else:
                    tab[i] = norm(pr[1] - pr[0], pr[1])
            facs.append(Factor(sc, tab))
            
        # Restrict evidence
        for f in facs:
            for e in range(N):
                if evid[e] < 0:
                    continue
                if e not in f.scope:
                    continue
                pos = f.scope.index(e)
                sz = len(f.scope)
                ln = 1 << sz
                ns = [f.scope[j] for j in range(sz) if j != pos]
                nt = []
                for i in range(ln):
                    bit = (i >> (sz - 1 - pos)) & 1
                    if bit == evid[e]:
                        nt.append(f.tab[i])
                f.scope = ns
                f.tab = nt
                
        # Eliminate hidden variables
        for v in range(N):
            if v == q or evid[v] >= 0:
                continue
            has = []
            rest = []
            for f in facs:
                if v in f.scope:
                    has.append(f)
                else:
                    rest.append(f)
            if not has:
                facs = rest
                continue
                
            sc = sorted(set(x for f in has for x in f.scope))
            sz = len(sc)
            ln = 1 << sz
            tab = [None] * ln
            for i in range(ln):
                pr = (1, 1)
                for f in has:
                    idx = 0
                    f_sz = len(f.scope)
                    for j in range(f_sz):
                        pos = sc.index(f.scope[j])
                        bit = (i >> (sz - 1 - pos)) & 1
                        idx |= (bit << (f_sz - 1 - j))
                    pr = mul(pr, f.tab[idx])
                tab[i] = pr
                
            pos = sc.index(v)
            ns = [sc[j] for j in range(sz) if j != pos]
            nt = [(0, 1)] * (1 << (sz - 1))
            for i in range(ln):
                ni = 0
                for j in range(sz):
                    if j == pos:
                        continue
                    bit = (i >> (sz - 1 - j)) & 1
                    ni = (ni << 1) | bit
                nt[ni] = add(nt[ni], tab[i])
            rest.append(Factor(ns, nt))
            facs = rest
            
        sc = sorted(set(x for f in facs for x in f.scope))
        sn = len(sc)
        szn = 1 << sn if sn > 0 else 1
        jt = (0, 1)
        jf = (0, 1)
        for i in range(szn):
            pr = (1, 1)
            for f in facs:
                idx = 0
                f_sz = len(f.scope)
                for j in range(f_sz):
                    pos = sc.index(f.scope[j])
                    bit = (i >> (sn - 1 - pos)) & 1
                    idx |= (bit << (f_sz - 1 - j))
                pr = mul(pr, f.tab[idx])
            if q in sc:
                ppos = sc.index(q)
                bit = (i >> (sn - 1 - ppos)) & 1
                if bit == 1:
                    jt = add(jt, pr)
                else:
                    jf = add(jf, pr)
                    
        tot = add(jt, jf)
        if tot[0] == 0:
            ans = (0, 1)
        else:
            ans = norm(jt[0] * tot[1], jt[1] * tot[0])
        out.append(f"VE {ans[0]}/{ans[1]}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
