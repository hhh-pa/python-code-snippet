import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        f = int(next(it))
        n = int(next(it))
    except StopIteration:
        return

    refs = [int(next(it)) for _ in range(n)]

    # OPT
    opt = 0
    frames_opt = []
    for i in range(n):
        r = refs[i]
        if r in frames_opt:
            continue
        opt += 1
        if len(frames_opt) < f:
            frames_opt.append(r)
            continue
        victim = 0
        far = -1
        for s, p in enumerate(frames_opt):
            nx = n + 1
            for j in range(i + 1, n):
                if refs[j] == p:
                    nx = j
                    break
            if nx > far:
                far = nx
                victim = s
        frames_opt[victim] = r

    # FIFO
    fifo = 0
    frames_fifo = []
    head = 0
    for i in range(n):
        r = refs[i]
        if r in frames_fifo:
            continue
        fifo += 1
        if len(frames_fifo) < f:
            frames_fifo.append(r)
        else:
            frames_fifo[head] = r
            head = (head + 1) % len(frames_fifo)

    # Clock
    clock = 0
    frames_clk = [0] * f
    occ = [False] * f
    ref = [False] * f
    hand = 0
    for i in range(n):
        r = refs[i]
        hit = False
        for s in range(f):
            if occ[s] and frames_clk[s] == r:
                hit = True
                ref[s] = True
                break
        if hit:
            continue
        clock += 1
        while True:
            if not occ[hand]:
                break
            if ref[hand]:
                ref[hand] = False
                hand = (hand + 1) % f
            else:
                break
        frames_clk[hand] = r
        occ[hand] = True
        ref[hand] = True
        hand = (hand + 1) % f

    # LRU
    lru = 0
    frames_lru = []
    for i in range(n):
        r = refs[i]
        try:
            at = frames_lru.index(r)
        except ValueError:
            at = -1
        if at != -1:
            p = frames_lru.pop(at)
            frames_lru.append(p)
            continue
        lru += 1
        if len(frames_lru) < f:
            frames_lru.append(r)
        else:
            frames_lru.pop(0)
            frames_lru.append(r)

    print(f"{opt} {fifo} {clock} {lru}")

if __name__ == "__main__":
    main()
