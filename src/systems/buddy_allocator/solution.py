import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        U = int(next(it))
        q = int(next(it))
    except StopIteration:
        return

    free_list = [set() for _ in range(U + 1)]
    free_list[U].add(0)
    alloc = {}

    for _ in range(q):
        op = int(next(it))
        if op == 1:
            s = int(next(it))
            if s < 1:
                print("FAIL")
                continue
            need = 0
            while need <= U and (1 << need) < s:
                need += 1
            found = -1
            at = 0
            for o in range(need, U + 1):
                if free_list[o]:
                    found = o
                    at = min(free_list[o])
                    break
            if need > U or found == -1:
                print("FAIL")
                continue
            free_list[found].remove(at)
            for o in range(found, need, -1):
                half = 1 << (o - 1)
                free_list[o - 1].add(at + half)
            alloc[at] = need
            print(at)
        elif op == 2:
            a = int(next(it))
            if a not in alloc:
                print("FAIL")
                continue
            o = alloc.pop(a)
            at = a
            while o < U:
                buddy = at ^ (1 << o)
                if buddy not in free_list[o]:
                    break
                free_list[o].remove(buddy)
                if buddy < at:
                    at = buddy
                o += 1
            free_list[o].add(at)
            print("OK")
        elif op == 3:
            print(" ".join(str(len(free_list[o])) for o in range(U + 1)))

if __name__ == "__main__":
    main()
