import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    q = int(tokens[1])
    idx = 2

    keys = [0] * m
    vals = [0] * m
    st = [0] * m  # 0 empty, 1 occupied, 2 tombstone

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
            start = h(k)
            tomb = -1
            found = -1
            for t in range(m):
                s = (start + t) % m
                if st[s] == 1 and keys[s] == k:
                    found = s
                    break
                if st[s] == 2 and tomb == -1:
                    tomb = s
                if st[s] == 0:
                    if tomb == -1:
                        tomb = s
                    break
            if found != -1:
                vals[found] = v
            elif tomb != -1:
                keys[tomb] = k
                vals[tomb] = v
                st[tomb] = 1
            else:
                out.append("FULL")
        elif op == 2:
            k = int(tokens[idx])
            idx += 1
            start = h(k)
            found = False
            ans = 0
            for t in range(m):
                s = (start + t) % m
                if st[s] == 0:
                    break
                if st[s] == 1 and keys[s] == k:
                    ans = vals[s]
                    found = True
                    break
            out.append(str(ans) if found else "NONE")
        elif op == 3:
            k = int(tokens[idx])
            idx += 1
            start = h(k)
            done = False
            for t in range(m):
                s = (start + t) % m
                if st[s] == 0:
                    break
                if st[s] == 1 and keys[s] == k:
                    st[s] = 2
                    done = True
                    break
            out.append("OK" if done else "NONE")
        elif op == 4:
            chars = []
            for s in range(m):
                if st[s] == 0:
                    chars.append(".")
                elif st[s] == 1:
                    chars.append("O")
                else:
                    chars.append("X")
            out.append("".join(chars))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
