import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    cs = []
    for _ in range(m):
        i = int(next(it))
        j = int(next(it))
        b = int(next(it))
        cs.append((i, j, b))

    d = [0] * n
    for _ in range(n):
        for i, j, b in cs:
            if d[i] + b < d[j]:
                d[j] = d[i] + b

    for i, j, b in cs:
        if d[i] + b < d[j]:
            print("INFEASIBLE")
            return

    print(" ".join(str(x) for x in d))

if __name__ == "__main__":
    main()
