import sys

def simulate_lcr(ring):
    n = len(ring)
    messages = 0
    for i in range(n):
        uid = ring[i]
        cur = i
        while True:
            messages += 1
            nxt = (cur + 1) % n
            if nxt == i:
                break
            if ring[nxt] > uid:
                break
            cur = nxt
    return messages

def simulate_hs(ring):
    n = len(ring)
    messages = 0
    phase = 0
    while True:
        limit = 1 << phase
        leader_found = False
        for i in range(n):
            uid = ring[i]
            for direction in (-1, 1):
                dist = 0
                cur = i
                ok = True
                while dist < limit:
                    dist += 1
                    messages += 1
                    cur = (cur + direction + n) % n
                    if cur == i:
                        leader_found = True
                        break
                    if ring[cur] > uid:
                        ok = False
                        break
                if leader_found:
                    break
                if ok:
                    messages += dist
            if leader_found:
                break
        if leader_found or limit >= n // 2:
            break
        phase += 1
    return messages

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
    except StopIteration:
        return

    ring = [int(next(it)) for _ in range(n)]
    leader_id = max(ring)

    lcr_msgs = simulate_lcr(ring)
    hs_msgs = simulate_hs(ring)

    out = [
        f"LEADER: {leader_id}",
        f"LCR MESSAGES: {lcr_msgs}",
        f"HS MESSAGES: {hs_msgs}",
    ]
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
