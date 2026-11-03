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
        N = int(next(it))
        M = int(next(it))
        B = int(next(it))
        
        bb = [0] * B
        bmask = [0] * B
        bv = [0] * B
        for i in range(B):
            bi = int(next(it))
            k = int(next(it))
            msk = 0
            for _ in range(k):
                msk |= 1 << int(next(it))
            v = int(next(it))
            bb[i] = bi
            bmask[i] = msk
            bv[i] = v
            
        def welfare(skip):
            best = 0
            bestm = 0
            limit = 1 << B
            for m in range(limit):
                used = 0
                tot = 0
                ok = True
                for i in range(B):
                    if not ((m >> i) & 1):
                        continue
                    if skip >= 0 and bb[i] == skip:
                        ok = False
                        break
                    if used & bmask[i]:
                        ok = False
                        break
                    used |= bmask[i]
                    tot += bv[i]
                if ok and tot > best:
                    best = tot
                    bestm = m
            won = [i for i in range(B) if (bestm >> i) & 1]
            return best, won

        W, won = welfare(-1)
        out.append(f"VCG {W}")
        pay_row = ["PAY"]
        for i in range(N):
            mine = sum(bv[w] for w in won if bb[w] == i)
            Wo, _ = welfare(i)
            pay_row.append(str(Wo - (W - mine)))
        out.append(" ".join(pay_row))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
