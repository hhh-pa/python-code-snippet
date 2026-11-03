import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    INF = int(4e14)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            x = int(next(it))
            L[i][j] = INF if x == 999999 else x
            
    m = 1
    while m < n - 1:
        N = [[INF] * n for _ in range(n)]
        for i in range(n):
            Li = L[i]
            for j in range(n):
                b = INF
                for k in range(n):
                    val = Li[k] + L[k][j]
                    if val < b:
                        b = val
                N[i][j] = b
        L = N
        m *= 2
        
    if n == 1:
        L[0][0] = 0
        
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            if L[i][j] >= INF // 2:
                row.append("INF")
            else:
                row.append(str(L[i][j]))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
