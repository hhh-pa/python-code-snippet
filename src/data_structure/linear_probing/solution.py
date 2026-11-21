import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if len(data) < 2 or data[0] <= 0 or data[1] < 0:
        return
    m, n = data[0], data[1]
    table = [None] * m
    for k in data[2 : 2 + n]:
        h = k % m
        for t in range(m):
            i = (h + t) % m
            if table[i] is None:
                table[i] = k
                break
    print(" ".join(str(v) if v is not None else "_" for v in table))


if __name__ == "__main__":
    main()
