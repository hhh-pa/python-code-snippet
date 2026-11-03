import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        S = int(next(it))
        E = int(next(it))
        B = int(next(it))
        n = int(next(it))
    except StopIteration:
        return

    sets = [[] for _ in range(S)]
    hits = 0
    misses = 0
    evict = 0

    for _ in range(n):
        addr = int(next(it))
        block = addr // B
        set_idx = block % S
        tag = block // S

        lines = sets[set_idx]
        try:
            at = lines.index(tag)
        except ValueError:
            at = -1

        if at != -1:
            hits += 1
            del lines[at]
            lines.insert(0, tag)
        else:
            misses += 1
            if len(lines) >= E:
                evict += 1
                lines.pop()
            lines.insert(0, tag)

    print(f"{hits} {misses} {evict}")

if __name__ == "__main__":
    main()
