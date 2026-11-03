import sys

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
        P = int(next(it))
        A = int(next(it))
        N = A + P
        pre = [0] * N
        add = [0] * N
        del_ = [0] * N
        
        for i in range(A):
            np = int(next(it))
            for _ in range(np):
                pre[i] |= 1 << int(next(it))
            na = int(next(it))
            for _ in range(na):
                add[i] |= 1 << int(next(it))
            nd = int(next(it))
            for _ in range(nd):
                del_[i] |= 1 << int(next(it))
                
        for p in range(P):
            pre[A + p] = 1 << p
            add[A + p] = 1 << p
            del_[A + p] = 0
            
        ni = int(next(it))
        initmask = 0
        for _ in range(ni):
            initmask |= 1 << int(next(it))
            
        ng = int(next(it))
        goalmask = 0
        for _ in range(ng):
            goalmask |= 1 << int(next(it))
            
        def bits_of(m):
            return [x for x in range(P) if (m >> x) & 1]
            
        actids = []
        amut = []
        pmodes = [initmask]
        pm0 = [[False] * P for _ in range(P)]
        pmut = [pm0]
        nogood = set()
        
        def amutex_at(lvl, a, b):
            if a > b:
                a, b = b, a
            return amut[lvl][a][b]
            
        def achievers(pr, lvl):
            return [a for a in actids[lvl] if (add[a] >> pr) & 1]
            
        def extract(k, goals):
            if k == 0:
                for g in goals:
                    if not ((initmask >> g) & 1):
                        return False, []
                return True, []
            gm = 0
            for g in goals:
                gm |= 1 << g
            key = (k << 32) | gm
            if key in nogood:
                return False, []
            ok, plan = cover(k, goals, [], 0)
            if not ok:
                nogood.add(key)
            return ok, plan
            
        def cover(k, unc, chosen, nextmask):
            if not unc:
                ok, sub = extract(k - 1, bits_of(nextmask))
                if not ok:
                    return False, []
                sub.append(list(chosen))
                return True, sub
            g = unc[0]
            for a in achievers(g, k - 1):
                if any(amutex_at(k - 1, a, c) for c in chosen):
                    continue
                nu = [x for x in unc if not ((add[a] >> x) & 1)]
                nc = chosen + [a]
                ok, plan = cover(k, nu, nc, nextmask | pre[a])
                if ok:
                    return True, plan
            return False, []
            
        solved = False
        plan = []
        solvedL = 0
        
        for L in range(13):
            if (pmodes[L] & goalmask) == goalmask:
                gs = bits_of(goalmask)
                mok = True
                for i in range(len(gs)):
                    for j in range(i + 1, len(gs)):
                        if pmut[L][gs[i]][gs[j]]:
                            mok = False
                            break
                    if not mok:
                        break
                if mok:
                    ok, pl = extract(L, gs)
                    if ok:
                        solved = True
                        plan = pl
                        solvedL = L
                        break
            if L == 12:
                break
                
            aids = [a for a in range(N) if (pre[a] & pmodes[L]) == pre[a]]
            am = [[False] * N for _ in range(N)]
            for i in range(len(aids)):
                x = aids[i]
                for j in range(i + 1, len(aids)):
                    y = aids[j]
                    mx = False
                    if (add[x] & del_[y]) or (add[y] & del_[x]):
                        mx = True
                    elif (del_[x] & pre[y]) or (del_[y] & pre[x]):
                        mx = True
                    else:
                        pa = bits_of(pre[x])
                        pb = bits_of(pre[y])
                        for u in pa:
                            for v in pb:
                                if pmut[L][u][v]:
                                    mx = True
                                    break
                            if mx:
                                break
                    am[x][y] = am[y][x] = mx
                    
            actids.append(aids)
            amut.append(am)
            
            nmask = 0
            for a in aids:
                nmask |= add[a]
                
            pm = [[False] * P for _ in range(P)]
            mc = 0
            for x in range(P):
                if not ((nmask >> x) & 1):
                    continue
                for y in range(x + 1, P):
                    if not ((nmask >> y) & 1):
                        continue
                    mx = True
                    for u in aids:
                        if not ((add[u] >> x) & 1):
                            continue
                        for v in aids:
                            if not ((add[v] >> y) & 1):
                                continue
                            if u == v or not am[u][v]:
                                mx = False
                                break
                        if not mx:
                            break
                    pm[x][y] = pm[y][x] = mx
                    if mx:
                        mc += 1
                        
            prevmc = 0
            for x in range(P):
                for y in range(x + 1, P):
                    if pmut[L][x][y]:
                        prevmc += 1
            same = (nmask == pmodes[L] and mc == prevmc)
            pmodes.append(nmask)
            pmut.append(pm)
            if same:
                break
                
        if not solved:
            out.append("GRAPHPLAN FAIL")
        else:
            out.append(f"GRAPHPLAN {solvedL}")
            for l in range(solvedL):
                ra = [a for a in plan[l] if a < A]
                ra.sort()
                out.append(" ".join(map(str, ra)))
                
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
