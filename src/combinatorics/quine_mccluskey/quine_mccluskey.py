import sys

def combine_pos(a, b):
    diff = -1
    for i in range(len(a)):
        if a[i] != b[i]:
            if a[i] == '-' or b[i] == '-':
                return -1
            if diff >= 0:
                return -1
            diff = i
    return diff

def covers(imp, mt):
    for i in range(len(imp)):
        if imp[i] != '-' and imp[i] != mt[i]:
            return False
    return True

def bits_of(m, n):
    return "".join('1' if ((m >> i) & 1) else '0' for i in range(n - 1, -1, -1))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    k = int(tokens[1])
    mts = sorted(set(int(tokens[2 + i]) for i in range(k)))
    
    cur = [bits_of(m, n) for m in mts]
    cur.sort()
    
    primes = []
    while True:
        groups = [[] for _ in range(n + 1)]
        for t in cur:
            c = t.count('1')
            groups[c].append(t)
            
        used = set()
        nxt = set()
        for g in range(n):
            for a in groups[g]:
                for b in groups[g + 1]:
                    d = combine_pos(a, b)
                    if d >= 0:
                        used.add(a)
                        used.add(b)
                        c = list(a)
                        c[d] = '-'
                        nxt.add("".join(c))
                        
        for t in cur:
            if t not in used:
                primes.append(t)
        if not nxt:
            break
        cur = sorted(nxt)
        
    primes = sorted(set(primes))
    mtbits = [bits_of(m, n) for m in mts]
    unc = [True] * len(mts)
    cover = set()
    
    for i in range(len(mts)):
        cov = [p for p in primes if covers(p, mtbits[i])]
        if len(cov) == 1:
            cover.add(cov[0])
            
    def apply_cover():
        for i in range(len(mts)):
            if unc[i]:
                for p in cover:
                    if covers(p, mtbits[i]):
                        unc[i] = False
                        break
                        
    apply_cover()
    while any(unc):
        best = None
        bc = -1
        for p in primes:
            c = sum(1 for i in range(len(mts)) if unc[i] and covers(p, mtbits[i]))
            if c > bc or (c == bc and (best is None or p < best)):
                best = p
                bc = c
        cover.add(best)
        apply_cover()
        
    covv = sorted(cover)
    sys.stdout.write(f"{len(primes)}\n{len(covv)}\n")
    for p in covv:
        sys.stdout.write(p + "\n")

if __name__ == "__main__":
    main()
