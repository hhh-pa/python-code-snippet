import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        f = int(next(it))
    except StopIteration:
        return

    init = [int(next(it)) for _ in range(n)]
    nf = int(next(it))
    faulty = [False] * n
    for _ in range(nf):
        faulty[int(next(it))] = True

    val = list(init)
    for ph in range(f + 1):
        king = ph % n
        nval = list(val)
        for i in range(n):
            if not faulty[i]:
                cnt = {}
                for j in range(n):
                    if not faulty[j]:
                        cnt[val[j]] = cnt.get(val[j], 0) + 1
                maj = -1
                mc = 0
                for k, v in cnt.items():
                    if v > mc:
                        mc = v
                        maj = k
                if mc >= n - f:
                    nval[i] = maj
                elif not faulty[king]:
                    nval[i] = val[king]
        val = nval

    out = []
    for i in range(n):
        if not faulty[i]:
            out.append(f"P{i}: {val[i]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
