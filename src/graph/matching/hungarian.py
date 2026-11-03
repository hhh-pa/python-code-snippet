import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    cost = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost[i][j] = int(next(it))

    INF = 10**18
    u = [0] * (n + 1)
    v = [0] * (m + 1)
    p = [0] * (m + 1)
    way = [0] * (m + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = 0

            cost_i0 = cost[i0]
            u_i0 = u[i0]
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost_i0[j] - u_i0 - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

            for j in range(0, m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    min_cost = -v[0]
    out = [str(min_cost)]
    match = [0] * (n + 1)
    for j in range(1, m + 1):
        if p[j] <= n:
            match[p[j]] = j

    for i in range(1, n + 1):
        out.append(f"{i} {match[i]}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
