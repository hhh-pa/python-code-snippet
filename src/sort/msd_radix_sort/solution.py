import sys

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n = int(lines[0].strip())
    a = lines[1 : 1 + n]
    a.sort()
    sys.stdout.write("[" + ",".join(a) + "]")

if __name__ == "__main__":
    main()
