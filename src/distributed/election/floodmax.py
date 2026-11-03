import collections
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        return

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    id_vals = [int(next(it)) for _ in range(n)]
    mx = max(id_vals)

    R = 0
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = collections.deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        for x in d:
            if x > R:
                R = x

    seen = list(id_vals)
    opt = 0
    send = [1] * n
    for r in range(1, R + 1):
        ns = list(seen)
        for i in range(n):
            if send[i]:
                opt += len(adj[i])
            for nb in adj[i]:
                if send[nb] and seen[nb] > ns[i]:
                    ns[i] = seen[nb]
        for i in range(n):
            send[i] = 1 if ns[i] != seen[i] else 0
        seen = ns

    out = [
        f"LEADER: {mx}",
        f"ROUNDS: {R}",
        f"FLOODMAX MESSAGES: {2 * m * R}",
        f"OPTFLOODMAX MESSAGES: {opt}",
    ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
