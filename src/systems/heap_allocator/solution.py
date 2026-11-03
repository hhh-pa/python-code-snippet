import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        H = int(next(it))
        q = int(next(it))
    except StopIteration:
        return

    sizes = []
    isfree = []
    if H >= 16:
        sizes.append(H)
        isfree.append(True)
    alloc = {}

    for _ in range(q):
        op = int(next(it))
        if op == 1:
            s = int(next(it))
            if s < 1:
                print("FAIL")
                continue
            need = s + 8
            pick = -1
            for k in range(len(sizes)):
                if isfree[k] and sizes[k] >= need:
                    pick = k
                    break
            if pick == -1:
                print("FAIL")
                continue
            leftover = sizes[pick] - need
            b = sum(sizes[:pick])
            if leftover >= 16:
                sizes[pick] = need
                sizes.insert(pick + 1, leftover)
                isfree.insert(pick + 1, True)
            isfree[pick] = False
            payload = b + 4
            alloc[payload] = sizes[pick]
            print(payload)
        elif op == 2:
            p = int(next(it))
            if p not in alloc:
                print("FAIL")
                continue
            del alloc[p]
            b = p - 4
            k = 0
            acc = 0
            for i in range(len(sizes)):
                if acc == b:
                    k = i
                    break
                acc += sizes[i]
            isfree[k] = True
            if k + 1 < len(sizes) and isfree[k + 1]:
                sizes[k] += sizes[k + 1]
                del sizes[k + 1]
                del isfree[k + 1]
            if k > 0 and isfree[k - 1]:
                sizes[k - 1] += sizes[k]
                del sizes[k]
                del isfree[k]
            print("OK")
        elif op == 3:
            print(" ".join(("F" if isfree[k] else "A") + str(sizes[k]) for k in range(len(sizes))))

if __name__ == "__main__":
    main()
