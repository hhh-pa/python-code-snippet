import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    r = int(next(it))
    avail = [int(next(it)) for _ in range(r)]
    alloc = [[int(next(it)) for _ in range(r)] for _ in range(n)]
    mx = [[int(next(it)) for _ in range(r)] for _ in range(n)]

    work = list(avail)
    done = [False] * n
    seq = []
    while True:
        pick = -1
        for i in range(n):
            if done[i]:
                continue
            ok = True
            for j in range(r):
                if mx[i][j] - alloc[i][j] > work[j]:
                    ok = False
                    break
            if ok:
                pick = i
                break
        if pick == -1:
            break
        done[pick] = True
        seq.append(pick)
        for j in range(r):
            work[j] += alloc[pick][j]

    if len(seq) == n:
        print("SAFE " + " ".join(map(str, seq)))
    else:
        print(f"UNSAFE {len(seq)}")

if __name__ == "__main__":
    main()
