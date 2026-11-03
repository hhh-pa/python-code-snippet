import sys
from functools import cmp_to_key

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    cap = float(tokens[1])
    v = [0] * n
    w = [0] * n
    idx = 2
    for i in range(n):
        v[i] = int(tokens[idx])
        w[i] = int(tokens[idx + 1])
        idx += 2
        
    order = list(range(n))
    def cmp(a, b):
        l = v[a] * w[b]
        r = v[b] * w[a]
        if l != r:
            return -1 if l > r else 1
        return -1 if a < b else 1
    order.sort(key=cmp_to_key(cmp))
    
    tot = 0.0
    rem = cap
    for i in order:
        if rem <= 0:
            break
        if w[i] <= rem:
            tot += v[i]
            rem -= w[i]
        else:
            tot += v[i] * (rem / w[i])
            rem = 0.0
    print(f"{tot:.6f}")

if __name__ == '__main__':
    main()
