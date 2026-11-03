import collections
import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    M = int(tokens[0])
    s = [int(tokens[1 + i]) for i in range(M)]
    
    cnt = collections.Counter(s)
    plug = 0.0
    for count in cnt.values():
        pr = count / M
        plug -= pr * math.log2(pr)
        
    dict_set = set()
    c = 0
    i = 0
    while i < M:
        j = i
        while j < M and tuple(s[i : j + 1]) in dict_set:
            j += 1
        if j >= M:
            c += 1
            break
        dict_set.add(tuple(s[i : j + 1]))
        c += 1
        i = j + 1
    lz = c * math.log2(M) / M
    
    l2n = math.log2(M)
    ky = 0.0
    nk = 0
    start = max(1, M // 2)
    for p in range(start, M):
        best = 0
        for q in range(p):
            L = 0
            while p + L < M and s[q + L] == s[p + L]:
                L += 1
            if L > best:
                best = L
        if best >= 1:
            ky += l2n / best
            nk += 1
    kyv = ky / nk if nk > 0 else l2n
    
    sys.stdout.write(f"PLUGIN: {plug:.6f}\n")
    sys.stdout.write(f"LZ: {lz:.6f}\n")
    sys.stdout.write(f"KY: {kyv:.6f}\n")

if __name__ == "__main__":
    main()
