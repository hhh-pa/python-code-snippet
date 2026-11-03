import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    syms = tokens[0]
    n = len(syms)
    ops = tokens[1] if n > 1 else ""
    
    T = [[0] * n for _ in range(n)]
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        if syms[i] == 'T':
            T[i][i] = 1
        else:
            F[i][i] = 1
            
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            t = 0
            f = 0
            for k in range(i, j):
                op = ops[k]
                lt, lf = T[i][k], F[i][k]
                rt, rf = T[k + 1][j], F[k + 1][j]
                tot = (lt + lf) * (rt + rf)
                if op == '&':
                    tt = lt * rt
                elif op == '|':
                    tt = tot - lf * rf
                else:
                    tt = lt * rf + lf * rt
                t += tt
                f += tot - tt
            T[i][j] = t
            F[i][j] = f
    print(T[0][n - 1])

if __name__ == '__main__':
    main()
