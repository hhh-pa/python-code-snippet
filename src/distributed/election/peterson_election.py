import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
    except StopIteration:
        return

    id_vals = [int(next(it)) for _ in range(n)]
    cur = list(id_vals)
    active = [1] * n
    leader = -1
    alias = -1
    phases = 0
    cap = 4 * n + 10

    while phases < cap:
        a = [i for i in range(n) if active[i]]
        k = len(a)
        if k == 0:
            break
        phases += 1
        if k == 1:
            leader = id_vals[a[0]]
            alias = cur[a[0]]
            break
        ncur = list(cur)
        nact = list(active)
        done = False
        for j in range(k):
            q = a[j]
            uid2 = cur[a[(j - 1 + k) % k]]
            uid3 = cur[a[(j - 2 + k) % k]]
            if uid2 == cur[q]:
                leader = id_vals[q]
                alias = cur[q]
                done = True
                break
            elif uid2 > cur[q] and uid2 > uid3:
                ncur[q] = uid2
            else:
                nact[q] = 0
        cur = ncur
        active = nact
        if done:
            break

    out = [
        f"LEADER: {leader}",
        f"ALIAS: {alias}",
        f"PHASES: {phases}",
        f"MESSAGES: {2 * n * phases}",
    ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
