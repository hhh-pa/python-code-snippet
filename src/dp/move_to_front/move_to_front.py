import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    lst = list(range(n))
    tot = 0
    idx = 2
    for _ in range(m):
        x = int(tokens[idx])
        idx += 1
        i = lst.index(x)
        tot += i + 1
        lst.pop(i)
        lst.insert(0, x)
    print(tot)

if __name__ == '__main__':
    main()
