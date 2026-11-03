import sys

def extgcd(a, b):
    if b == 0:
        x = 1 if a >= 0 else -1
        return (a if a >= 0 else -a), x, 0
    g, x1, y1 = extgcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a = int(tokens[0])
    b = int(tokens[1])
    if a == 0 and b == 0:
        print("0 0 0")
        return

    aa = abs(a)
    bb = abs(b)
    g, x, y = extgcd(aa, bb)
    if a < 0:
        x = -x
    if b < 0:
        y = -y

    print(f"{g} {x} {y}")

if __name__ == '__main__':
    main()
