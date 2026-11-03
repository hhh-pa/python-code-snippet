import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    k = int(next(it))
    strs = [next(it) for _ in range(k)]

    if k == 0:
        print("0\n")
        return
    if k == 1:
        print(f"{len(strs[0])}\n{strs[0]}")
        return

    hi = min(len(s) for s in strs)

    def has_common(L):
        if L == 0:
            return True, ""
        common = set(strs[0][i:i + L] for i in range(len(strs[0]) - L + 1))
        for t in range(1, k):
            st = strs[t]
            cur = set()
            for i in range(len(st) - L + 1):
                sub = st[i:i + L]
                if sub in common:
                    cur.add(sub)
            common = cur
            if not common:
                return False, ""
        return True, next(iter(common))

    best = 0
    best_str = ""
    low = 0
    high = hi

    while low <= high:
        mid = (low + high) // 2
        ok, cur = has_common(mid)
        if ok:
            best = mid
            best_str = cur
            low = mid + 1
        else:
            high = mid - 1

    if best > 0:
        common = set(strs[0][i:i + best] for i in range(len(strs[0]) - best + 1))
        for t in range(1, k):
            st = strs[t]
            cur = set()
            for i in range(len(st) - best + 1):
                sub = st[i:i + best]
                if sub in common:
                    cur.add(sub)
            common = cur
        best_str = min(common)

    print(best)
    print(best_str)

if __name__ == "__main__":
    main()
