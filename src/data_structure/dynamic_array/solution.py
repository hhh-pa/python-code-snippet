import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    a = []
    cap = 1
    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            if len(a) == cap:
                cap *= 2
            a.append(x)
        elif op == 2:
            if not a:
                out.append("EMPTY")
            else:
                out.append(str(a.pop()))
                if len(a) > 0 and len(a) * 4 <= cap and cap > 1:
                    cap //= 2
        elif op == 3:
            j = int(tokens[idx])
            idx += 1
            if j < 0 or j >= len(a):
                out.append("NONE")
            else:
                out.append(str(a[j]))
        elif op == 4:
            out.append(f"{len(a)} {cap}")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
