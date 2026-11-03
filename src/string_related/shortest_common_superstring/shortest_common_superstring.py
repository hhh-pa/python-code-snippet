import sys

def overlap(a, b):
    max_k = min(len(a), len(b))
    for k in range(max_k, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    strs = [next(it) for _ in range(n)]

    while len(strs) > 1:
        best_i = -1
        best_j = -1
        best_ov = -1
        best_merged = ""

        sz = len(strs)
        for i in range(sz):
            for j in range(sz):
                if i == j:
                    continue
                ov = overlap(strs[i], strs[j])
                if ov > best_ov:
                    best_ov = ov
                    best_i = i
                    best_j = j
                    best_merged = strs[i] + strs[j][ov:]

        nxt = [strs[k] for k in range(sz) if k != best_i and k != best_j]
        nxt.append(best_merged)
        strs = nxt

    print(strs[0])

if __name__ == "__main__":
    main()
