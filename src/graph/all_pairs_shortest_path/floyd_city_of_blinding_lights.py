import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    it = iter(input_data)
    n = int(next(it))
    m = int(next(it))
    
    INF = 999999
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][i] = 0
        
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        wt = int(next(it))
        d[u][v] = wt
        
    for k in range(1, n + 1):
        dk = d[k]
        for i in range(1, n + 1):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(1, n + 1):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
                    
    q = int(next(it))
    out = []
    for _ in range(q):
        a = int(next(it))
        b = int(next(it))
        ans = d[a][b]
        if ans >= INF:
            out.append("-1")
        else:
            out.append(str(ans))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
