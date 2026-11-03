import sys

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a = int(tokens[0])
    b = int(tokens[1])
    n = int(tokens[2])

    if n <= 0:
        print("NONE")
        return
    if n == 1:
        print("0")
        return

    a = ((a % n) + n) % n
    b = ((b % n) + n) % n

    g, x, y = egcd(a, n)
    if b % g != 0:
        print("NONE")
        return

    n2 = n // g
    x0 = (x * (b // g) % n + n) % n
    sols = [(x0 + k * n2) % n for k in range(g)]
    sols.sort()

    print(g)
    print(*(sols))

if __name__ == '__main__':
    main()
