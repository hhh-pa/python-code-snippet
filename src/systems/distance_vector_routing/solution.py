import sys

INFLL = 4000000000000000000

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        N = int(next(it))
        E = int(next(it))
    except StopIteration:
        return

    cost = [[INFLL] * N for _ in range(N)]
    nbr = [[] for _ in range(N)]
    for _ in range(E):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        cost[u][v] = c
        cost[v][u] = c
        nbr[u].append(v)
        nbr[v].append(u)

    dist = [[INFLL] * N for _ in range(N)]
    nx = [[-1] * N for _ in range(N)]
    for i in range(N):
        dist[i][i] = 0
        nx[i][i] = i
        for nb in nbr[i]:
            dist[i][nb] = cost[i][nb]
            nx[i][nb] = nb

    rounds = 0
    for _ in range(1000):
        changed = False
        nd = [row[:] for row in dist]
        nn = [row[:] for row in nx]
        for i in range(N):
            for d in range(N):
                if d == i:
                    continue
                best = INFLL
                bn = -1
                for nb in nbr[i]:
                    a = INFLL if (nx[nb][d] == i and d != nb) else dist[nb][d]
                    cand = INFLL if a >= INFLL // 2 else cost[i][nb] + a
                    if cand < best or (cand == best and (bn == -1 or nb < bn)):
                        best = cand
                        bn = nb
                if best != dist[i][d] or bn != nx[i][d]:
                    nd[i][d] = best
                    nn[i][d] = bn
                    changed = True
        dist = nd
        nx = nn
        if not changed:
            break
        rounds += 1

    print(rounds)
    dst = N - 1
    for i in range(N):
        if i == dst:
            print("0 -")
        elif dist[i][dst] >= INFLL // 2:
            print("INF -")
        else:
            print(f"{dist[i][dst]} {nx[i][dst]}")

if __name__ == "__main__":
    main()
