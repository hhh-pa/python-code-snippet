import sys
from collections import defaultdict

sys.setrecursionlimit(200000)

def solve_sts(v):
    trips = []
    by_pair = defaultdict(list)
    for a in range(v):
        for b in range(a + 1, v):
            for c in range(b + 1, v):
                ti = len(trips)
                trips.append((a, b, c))
                by_pair[(a, b)].append(ti)
                by_pair[(a, c)].append(ti)
                by_pair[(b, c)].append(ti)
                
    covered = [[False] * v for _ in range(v)]
    chosen = []
    need = v * (v - 1) // 6
    
    def bt():
        if len(chosen) == need:
            return True
        fa = -1
        fb = -1
        for a in range(v):
            for b in range(a + 1, v):
                if not covered[a][b]:
                    fa = a
                    fb = b
                    break
            if fa >= 0:
                break
                
        for ti in by_pair[(fa, fb)]:
            t = trips[ti]
            ps = ((t[0], t[1]), (t[0], t[2]), (t[1], t[2]))
            if covered[ps[0][0]][ps[0][1]] or covered[ps[1][0]][ps[1][1]] or covered[ps[2][0]][ps[2][1]]:
                continue
            for p0, p1 in ps:
                covered[p0][p1] = True
            chosen.append(t)
            if bt():
                return True
            chosen.pop()
            for p0, p1 in ps:
                covered[p0][p1] = False
        return False

    bt()
    chosen.sort()
    return chosen

def solve_kts(v, chosen):
    per = v // 3
    nc = (len(chosen) + per - 1) // per
    classes = [[] for _ in range(nc)]
    used_masks = [0] * nc
    T = len(chosen)
    
    def kbt(i):
        if i == T:
            return all(len(c) == per for c in classes)
        t = chosen[i]
        t_mask = (1 << t[0]) | (1 << t[1]) | (1 << t[2])
        for idx_c in range(nc):
            c = classes[idx_c]
            if len(c) >= per:
                continue
            if used_masks[idx_c] & t_mask:
                continue
            c.append(t)
            used_masks[idx_c] |= t_mask
            if kbt(i + 1):
                return True
            c.pop()
            used_masks[idx_c] &= ~t_mask
            if not c:
                break
        return False

    kbt(0)
    return classes

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode in ("S", "K"):
        v = int(tokens[1])
        chosen = solve_sts(v)
        if mode == "S":
            for t in chosen:
                sys.stdout.write(f"{t[0]} {t[1]} {t[2]}\n")
        else:
            classes = solve_kts(v, chosen)
            for c in classes:
                c.sort()
                row = []
                for t in c:
                    row.extend([str(t[0]), str(t[1]), str(t[2])])
                sys.stdout.write(" ".join(row) + "\n")
    else:
        v = int(tokens[1])
        t = int(tokens[2])
        idx = 3
        tr = []
        for _ in range(t):
            tr.append((int(tokens[idx]), int(tokens[idx+1]), int(tokens[idx+2])))
            idx += 3
        valid = (len(tr) == v * (v - 1) // 6)
        seen = set()
        for a, b, c in tr:
            if not (0 <= a < b < c < v):
                valid = False
            for p in ((a, b), (a, c), (b, c)):
                if p in seen:
                    valid = False
                seen.add(p)
        if len(seen) != v * (v - 1) // 2:
            valid = False
        sys.stdout.write("VALID\n" if valid else "INVALID\n")

if __name__ == "__main__":
    main()
