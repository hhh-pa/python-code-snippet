import math
import sys

def cvar(S, items, iv):
    wsum = sum(iv[i] for i in items)
    v = 0.0
    for i in items:
        wi = iv[i] / wsum
        for j in items:
            v += wi * (iv[j] / wsum) * S[i][j]
    return v

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    S = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            S[i][j] = float(tokens[idx])
            idx += 1
            
    sd = [math.sqrt(S[i][i]) for i in range(n)]
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rho = S[i][j] / (sd[i] * sd[j])
            rho = max(-1.0, min(1.0, rho))
            D[i][j] = math.sqrt(max(0.0, 0.5 * (1.0 - rho)))
            
    total_nodes = 2 * n - 1
    members = [[i] for i in range(n)] + [[] for _ in range(n - 1)]
    alive = [True] * n + [False] * (n - 1)
    CD = [[1e100] * total_nodes for _ in range(total_nodes)]
    for i in range(n):
        for j in range(n):
            CD[i][j] = D[i][j]
            
    L = [-1] * total_nodes
    R = [-1] * total_nodes
    next_node = n
    
    for _ in range(n - 1):
        best = 1e100
        bi, bj = -1, -1
        for i in range(next_node):
            if not alive[i]:
                continue
            for j in range(i + 1, next_node):
                if not alive[j]:
                    continue
                if CD[i][j] < best:
                    best = CD[i][j]
                    bi, bj = i, j
        alive[bi] = False
        alive[bj] = False
        alive[next_node] = True
        L[next_node] = bi
        R[next_node] = bj
        members[next_node] = members[bi] + members[bj]
        for i in range(next_node):
            if alive[i]:
                dd = min(CD[bi][i], CD[bj][i])
                CD[next_node][i] = CD[i][next_node] = dd
        next_node += 1
        
    order = []
    tmp = [2 * n - 2]
    while tmp:
        u = tmp.pop()
        if u < n:
            order.append(u)
        else:
            tmp.append(R[u])
            tmp.append(L[u])
            
    iv = [1.0 / S[i][i] for i in range(n)]
    wt = [1.0] * n
    work = [list(order)]
    while work:
        cur = work.pop()
        if len(cur) < 2:
            continue
        mid = len(cur) // 2
        Lc = cur[:mid]
        Rc = cur[mid:]
        vl = cvar(S, Lc, iv)
        vr = cvar(S, Rc, iv)
        a = 1.0 - vl / (vl + vr)
        for i in Lc:
            wt[i] *= a
        for i in Rc:
            wt[i] *= (1.0 - a)
        work.append(Lc)
        work.append(Rc)
        
    ws = sum(wt)
    order_str = " ".join(str(x) for x in order)
    weights_str = " ".join(f"{x / ws:.6f}" for x in wt)
    sys.stdout.write(f"ORDER: {order_str}\n")
    sys.stdout.write(f"WEIGHTS: {weights_str}\n")

if __name__ == "__main__":
    main()
