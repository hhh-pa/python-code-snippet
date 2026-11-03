import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    a.sort()
    sys.stdout.write("[" + ",".join(str(x) for x in a) + "]")

if __name__ == "__main__":
    main()
