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
    for _ in range(E):
        u = int(next(it))
        v = int(next(it))
        c = int(next(it))
        cost[u][v] = c
        cost[v][u] = c

    out_lines = []
    for s in range(N):
        dist = [INFLL] * N
        parent = [-1] * N
        done = [False] * N
        dist[s] = 0

        for _ in range(N):
            u = -1
            for i in range(N):
                if not done[i] and (u == -1 or dist[i] < dist[u]):
                    u = i
            if u == -1 or dist[u] == INFLL:
                break
            done[u] = True
            dist_u = dist[u]
            cost_u = cost[u]
            for v in range(N):
                c = cost_u[v]
                if c < INFLL // 2 and dist_u + c < dist[v]:
                    dist[v] = dist_u + c
                    parent[v] = u

        line_tokens = []
        for d in range(N):
            if d == s:
                line_tokens.append("0:-")
            elif dist[d] >= INFLL // 2:
                line_tokens.append("INF:-")
            else:
                x = d
                while parent[x] != s:
                    x = parent[x]
                line_tokens.append(f"{dist[d]}:{x}")
        out_lines.append(" ".join(line_tokens))

    sys.stdout.write("\n".join(out_lines) + "\n")

if __name__ == "__main__":
    main()
