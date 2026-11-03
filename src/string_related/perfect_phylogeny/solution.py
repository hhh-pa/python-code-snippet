import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    rows = [next(it) for _ in range(n)]

    cols = [[int(rows[i][j]) for i in range(n)] for j in range(m)]

    for j in range(m):
        col_j = cols[j]
        for k in range(j + 1, m):
            col_k = cols[k]
            h11 = False
            h10 = False
            h01 = False
            for i in range(n):
                a = col_j[i]
                b = col_k[i]
                if a == 1 and b == 1:
                    h11 = True
                elif a == 1:
                    h10 = True
                elif b == 1:
                    h01 = True
                if h11 and h10 and h01:
                    print("NO")
                    return

    print("YES")

if __name__ == "__main__":
    main()
