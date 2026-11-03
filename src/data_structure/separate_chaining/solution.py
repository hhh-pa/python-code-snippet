import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    q = int(tokens[1])
    idx = 2

    # buckets: list of list of [key, val]
    t = [[] for _ in range(m)]

    def h(k):
        return k % m

    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            k = int(tokens[idx])
            v = int(tokens[idx + 1])
            idx += 2
            b = t[h(k)]
            found = False
            for pair in b:
                if pair[0] == k:
                    pair[1] = v
                    found = True
                    break
            if not found:
                b.append([k, v])
        elif op == 2:
            k = int(tokens[idx])
            idx += 1
            b = t[h(k)]
            found = False
            ans = 0
            for pair in b:
                if pair[0] == k:
                    ans = pair[1]
                    found = True
                    break
            out.append(str(ans) if found else "NONE")
        elif op == 3:
            k = int(tokens[idx])
            idx += 1
            b = t[h(k)]
            done = False
            for j in range(len(b)):
                if b[j][0] == k:
                    b[j] = b[-1]
                    b.pop()
                    done = True
                    break
            out.append("OK" if done else "NONE")
        elif op == 4:
            sizes = [str(len(b)) for b in t]
            out.append(" ".join(sizes))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
