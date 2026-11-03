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

def cmpf(a, b):
    l = a[0] * b[1]
    r = b[0] * a[1]
    if l < r:
        return -1
    if l > r:
        return 1
    return 0

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
        D = int(next(it))
        types = next(it)
        n = 1 << D
        leaves = [int(next(it)) for _ in range(n)]
        
        def solve(idx, level):
            if level == len(types):
                return norm(leaves[idx], 1)
            a = solve(idx * 2, level + 1)
            b = solve(idx * 2 + 1, level + 1)
            t = types[level]
            if t == 'X':
                return a if cmpf(a, b) >= 0 else b
            if t == 'N':
                return a if cmpf(a, b) <= 0 else b
            return norm(a[0] * b[1] + b[0] * a[1], 2 * a[1] * b[1])
            
        r = solve(0, 0)
        out.append(f"EXPECTI {r[0]}/{r[1]}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
