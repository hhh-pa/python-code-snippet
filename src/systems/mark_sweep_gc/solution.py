import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        r = int(next(it))
    except StopIteration:
        return

    roots = [int(next(it)) for _ in range(r)]
    refs = []
    for _ in range(n):
        k = int(next(it))
        refs.append([int(next(it)) for _ in range(k)])

    marked = [False] * n
    stack = []
    for rt in roots:
        if rt < 0 or rt >= n or marked[rt]:
            continue
        marked[rt] = True
        stack.append(rt)
        while stack:
            u = stack.pop()
            for v in refs[u]:
                if v < 0 or v >= n or marked[v]:
                    continue
                marked[v] = True
                stack.append(v)

    freed = [i for i in range(n) if not marked[i]]
    if not freed:
        print("NONE")
    else:
        print(" ".join(map(str, freed)))

if __name__ == "__main__":
    main()
