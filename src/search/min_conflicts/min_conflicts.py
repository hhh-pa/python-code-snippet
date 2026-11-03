import sys

def conflicts_at(b, row, col):
    n = len(b)
    c = 0
    for i in range(n):
        if i == row:
            continue
        bi = b[i]
        if bi == col:
            c += 1
        elif abs(bi - col) == abs(i - row):
            c += 1
    return c

def total_pairs(b):
    n = len(b)
    c = 0
    for i in range(n):
        bi = b[i]
        for j in range(i + 1, n):
            bj = b[j]
            if bi == bj:
                c += 1
            elif abs(bi - bj) == j - i:
                c += 1
    return c

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
        MS = int(next(it))
        b = [int(next(it)) for _ in range(N)]
        
        for _ in range(MS):
            vr = -1
            vc = -1
            for i in range(N):
                c = conflicts_at(b, i, b[i])
                if c > 0 and c > vc:
                    vc = c
                    vr = i
            if vr < 0:
                break
                
            bc = b[vr]
            bv = conflicts_at(b, vr, bc)
            for c in range(N):
                v = conflicts_at(b, vr, c)
                if v < bv:
                    bv = v
                    bc = c
            b[vr] = bc
            
        out.append(" ".join(map(str, b)))
        out.append(str(total_pairs(b)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
