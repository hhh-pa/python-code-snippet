import sys

sys.setrecursionlimit(200000)

def gen(rem, maxv, pre, out):
    if rem == 0:
        out.append(" ".join(map(str, pre)))
        return
    limit = maxv if maxv < rem else rem
    for v in range(limit, 0, -1):
        pre.append(v)
        gen(rem - v, v, pre, out)
        pre.pop()

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "G":
        n = int(tokens[1])
        out = []
        gen(n, n, [], out)
        sys.stdout.write("\n".join(out) + "\n")
    else:
        k = int(tokens[1])
        p = [int(tokens[2 + i]) for i in range(k)]
        if not p:
            return
        c = []
        for j in range(p[0]):
            cnt = sum(1 for x in p if x > j)
            c.append(cnt)
        sys.stdout.write(" ".join(map(str, c)) + "\n")

if __name__ == "__main__":
    main()
