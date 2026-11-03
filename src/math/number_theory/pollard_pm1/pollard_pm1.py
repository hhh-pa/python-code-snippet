import math
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    B = int(tokens[1])

    if n <= 1:
        print("NONE")
        return

    a = 2
    for k in range(2, B + 1):
        a = pow(a, k, n)
        diff = (a - 1 + n) if a > 0 else (n - 1)
        g = math.gcd(diff, n)
        if 1 < g < n:
            print(g)
            return

    g = math.gcd((a - 1 + n) % n, n)
    if 1 < g < n:
        print(g)
        return

    print("NONE")

if __name__ == '__main__':
    main()
