import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    
    t = [[0] * n for _ in range(n)]
    for i in range(n):
        t[i][i] = 1
        
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        t[u][v] = 1
        
    for k in range(n):
        tk = t[k]
        for i in range(n):
            if t[i][k]:
                ti = t[i]
                for j in range(n):
                    if tk[j]:
                        ti[j] = 1
                        
    out = []
    for i in range(n):
        out.append(" ".join(str(x) for x in t[i]))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
