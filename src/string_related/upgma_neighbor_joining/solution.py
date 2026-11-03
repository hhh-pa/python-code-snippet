import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    N = 2 * n

    d0 = [[0.0] * N for _ in range(N)]
    for i in range(n):
        for j in range(n):
            d0[i][j] = float(next(it))

    out = []

    # UPGMA
    d = [row[:] for row in d0]
    sz = [1] * N
    on = [False] * N
    for i in range(n):
        on[i] = True
    cnt = n
    nid = n

    while cnt > 1:
        bi = -1
        bj = -1
        bd = 0.0
        first = True
        for i in range(nid):
            if on[i]:
                for j in range(i + 1, nid):
                    if on[j]:
                        if first or d[i][j] < bd:
                            first = False
                            bd = d[i][j]
                            bi = i
                            bj = j

        out.append(f"{bi} {bj}")
        sz_sum = sz[bi] + sz[bj]
        for k in range(nid):
            if on[k] and k != bi and k != bj:
                v = (sz[bi] * d[bi][k] + sz[bj] * d[bj][k]) / sz_sum
                d[nid][k] = d[k][nid] = v

        sz[nid] = sz_sum
        on[bi] = on[bj] = False
        on[nid] = True
        nid += 1
        cnt -= 1

    # Neighbor-Joining
    d = [row[:] for row in d0]
    on = [False] * N
    for i in range(n):
        on[i] = True
    cnt = n
    nid = n
    R = [0.0] * N

    while cnt > 2:
        for i in range(nid):
            if on[i]:
                R[i] = sum(d[i][k] for k in range(nid) if on[k])

        bi = -1
        bj = -1
        bq = 0.0
        first = True
        for i in range(nid):
            if on[i]:
                for j in range(i + 1, nid):
                    if on[j]:
                        q = (cnt - 2) * d[i][j] - R[i] - R[j]
                        if first or q < bq:
                            first = False
                            bq = q
                            bi = i
                            bj = j

        out.append(f"{bi} {bj}")
        for k in range(nid):
            if on[k] and k != bi and k != bj:
                v = (d[bi][k] + d[bj][k] - d[bi][bj]) / 2.0
                d[nid][k] = d[k][nid] = v

        on[bi] = on[bj] = False
        on[nid] = True
        nid += 1
        cnt -= 1

    a = -1
    b = -1
    for i in range(nid):
        if on[i]:
            if a < 0:
                a = i
            else:
                b = i
    out.append(f"{a} {b}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
