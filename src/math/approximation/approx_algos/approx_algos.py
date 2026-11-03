import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    idx = 1
    if mode == "VC":
        n = int(tokens[idx])
        m = int(tokens[idx + 1])
        idx += 2
        U = [0] * m
        V = [0] * m
        for i in range(m):
            U[i] = int(tokens[idx])
            V[i] = int(tokens[idx + 1])
            idx += 2
        cov = [False] * n
        for i in range(m):
            u, v = U[i], V[i]
            if not cov[u] and not cov[v]:
                cov[u] = True
                cov[v] = True
        out = [i for i in range(n) if cov[i]]
        print(len(out))
        print(*(out))
    elif mode == "SC":
        n = int(tokens[idx])
        m = int(tokens[idx + 1])
        idx += 2
        sets = []
        for _ in range(m):
            k = int(tokens[idx])
            idx += 1
            sets.append([int(x) for x in tokens[idx : idx + k]])
            idx += k
        unc = [True] * n
        left = n
        chosen = []
        while left > 0:
            best = -1
            bi = -1
            for i in range(m):
                cnt = sum(1 for e in sets[i] if unc[e])
                if cnt > best:
                    best = cnt
                    bi = i
            if best <= 0:
                break
            chosen.append(bi)
            for e in sets[bi]:
                if unc[e]:
                    unc[e] = False
                    left -= 1
        print(len(chosen))
        print(*(chosen))
    elif mode == "TSP":
        n = int(tokens[idx])
        idx += 1
        d = []
        for _ in range(n):
            d.append([int(x) for x in tokens[idx : idx + n]])
            idx += n
        vis = [False] * n
        tour = [0]
        vis[0] = True
        cur = 0
        total = 0
        for _ in range(n - 1):
            best = -1
            bi = -1
            for j in range(n):
                if not vis[j] and (best < 0 or d[cur][j] < best):
                    best = d[cur][j]
                    bi = j
            tour.append(bi)
            vis[bi] = True
            total += best
            cur = bi
        total += d[cur][0]
        tour.append(0)
        print(*(tour))
        print(total)
    elif mode == "SS":
        n = int(tokens[idx])
        target = int(tokens[idx + 1])
        eps = float(tokens[idx + 2])
        idx += 3
        vals = [int(tokens[idx + i]) for i in range(n)]
        delta = eps / (2 * n)
        L = [0]
        for x in vals:
            M = set(L)
            for v in L:
                if v + x <= target:
                    M.add(v + x)
            mv = sorted(M)
            nl = [mv[0]]
            last = mv[0]
            for i in range(1, len(mv)):
                if mv[i] > last * (1 + delta):
                    nl.append(mv[i])
                    last = mv[i]
            L = nl
        print(L[-1])

if __name__ == '__main__':
    main()
