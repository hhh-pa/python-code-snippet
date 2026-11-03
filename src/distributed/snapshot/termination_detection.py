import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        E = int(next(it))
    except StopIteration:
        return

    engaged = [0] * n
    parent = [-1] * n
    idlepend = [0] * n
    C = [0] * n
    D = [0] * n
    engaged[0] = 1
    signals = 0
    ignored = 0
    term_at = -1

    ev = []
    a = []
    b = []
    for _ in range(E):
        op = next(it)
        ev.append(op)
        if op == "SEND":
            a.append(int(next(it)))
            b.append(int(next(it)))
        else:
            a.append(int(next(it)))
            b.append(0)

    for k in range(E):
        e = k + 1
        if term_at >= 0:
            break
        if ev[k] == "SEND":
            u = a[k]
            v = b[k]
            if not engaged[u]:
                ignored += 1
                continue
            D[u] += 1
            if not engaged[v]:
                engaged[v] = 1
                parent[v] = u
                C[u] += 1
            else:
                D[u] -= 1
                signals += 1
        else:
            i = a[k]
            if not engaged[i]:
                continue
            engaged[i] = 0
            x = i
            while True:
                if D[x] > 0:
                    idlepend[x] = 1
                    break
                idlepend[x] = 0
                if x == 0:
                    if C[0] == 0:
                        term_at = e
                    break
                p = parent[x]
                C[p] -= 1
                D[p] -= 1
                signals += 1
                if engaged[p]:
                    break
                x = p

    out = []
    if term_at >= 0:
        out.append(f"TERMINATED: {term_at}")
    else:
        out.append("TERMINATED: NEVER")
    out.append(f"SIGNALS: {signals}")
    out.append(f"IGNORED: {ignored}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
