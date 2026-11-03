import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    t = s + "$"
    n = len(t)
    sa = list(range(n))
    sa.sort(key=lambda a: t[a:])
    bwt = [t[(sa[i] - 1 + n) % n] for i in range(n)]
    print("".join(bwt))

if __name__ == "__main__":
    main()
