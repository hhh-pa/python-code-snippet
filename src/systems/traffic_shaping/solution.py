import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        policy = int(next(it))
    except StopIteration:
        return

    if policy == 0:
        rate = int(next(it))
        depth = int(next(it))
        n = int(next(it))
        toks = depth
        last = 0
        first = True
        out = []
        for _ in range(n):
            t = int(next(it))
            s = int(next(it))
            if first:
                last = t
                first = False
            toks += rate * (t - last)
            if toks > depth:
                toks = depth
            last = t
            if toks >= s:
                toks -= s
                out.append("CONFORM")
            else:
                out.append("DROP")
        sys.stdout.write("\n".join(out) + "\n")
    elif policy == 1:
        rate = int(next(it))
        depth = int(next(it))
        n = int(next(it))
        content = 0
        last = 0
        first = True
        out = []
        for _ in range(n):
            t = int(next(it))
            s = int(next(it))
            if first:
                last = t
                first = False
            content -= rate * (t - last)
            if content < 0:
                content = 0
            last = t
            if content + s <= depth:
                content += s
                out.append("CONFORM")
            else:
                out.append("DROP")
        sys.stdout.write("\n".join(out) + "\n")
    else:
        F = int(next(it))
        n = int(next(it))
        w = [int(next(it)) for _ in range(F)]
        L = 1
        for x in w:
            L = L // math.gcd(L, x) * x

        pk = []
        for _ in range(n):
            flow = int(next(it))
            arr = int(next(it))
            size = int(next(it))
            pk.append((flow, arr, size))

        prev_f = [0] * F
        fnum = [0] * n
        for i in range(n):
            flow, arr, size = pk[i]
            start = arr * L
            if prev_f[flow] > start:
                start = prev_f[flow]
            fin = start + size * (L // w[flow])
            prev_f[flow] = fin
            fnum[i] = fin

        out = []
        for i in range(n):
            out.append(f"{fnum[i]}/{L}")
        ord_idx = sorted(range(n), key=lambda x: (fnum[x], pk[x][0], x))
        out.append("ORDER " + " ".join(map(str, ord_idx)))
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
