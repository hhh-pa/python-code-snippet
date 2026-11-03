from collections import OrderedDict, deque
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    f = int(tokens[0])
    m = int(tokens[1])
    rq = [int(x) for x in tokens[2 : 2 + m]]

    # FIFO
    ff = 0
    fq = deque()
    fs = set()
    for p in rq:
        if f <= 0:
            ff += 1
            continue
        if p in fs:
            continue
        ff += 1
        if len(fq) >= f:
            fs.remove(fq.popleft())
        fq.append(p)
        fs.add(p)

    # LRU
    lf = 0
    lru = OrderedDict()
    for p in rq:
        if f <= 0:
            lf += 1
            continue
        if p in lru:
            lru.move_to_end(p)
            continue
        lf += 1
        if len(lru) >= f:
            lru.popitem(last=False)
        lru[p] = True

    # MARKING
    mf = 0
    cache = set()
    marked = set()
    rng = 42

    def rnd():
        nonlocal rng
        rng = (1103515245 * rng + 12345) % (1 << 31)
        return rng

    for p in rq:
        if f <= 0:
            mf += 1
            continue
        if p in cache:
            marked.add(p)
            continue
        mf += 1
        if len(cache) < f:
            cache.add(p)
            marked.add(p)
            continue
        if len(marked) >= len(cache):
            marked.clear()
        cands = sorted(c for c in cache if c not in marked)
        ev = cands[rnd() % len(cands)]
        cache.remove(ev)
        marked.discard(ev)
        cache.add(p)
        marked.add(p)

    print(ff)
    print(lf)
    print(mf)

if __name__ == '__main__':
    main()
