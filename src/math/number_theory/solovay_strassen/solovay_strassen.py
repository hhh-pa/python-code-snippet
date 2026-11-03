import math
import sys

def jacobi(a, n):
    a %= n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r in (3, 5):
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a %= n
    return t if n == 1 else 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    t = int(tokens[1])
    b = [int(tokens[2 + i]) for i in range(t)]

    js = [0] * t
    comp = False

    if n < 2:
        comp = True
    elif n == 2:
        for i in range(t):
            js[i] = jacobi(b[i], n)
    elif n % 2 == 0:
        comp = True
    else:
        for i in range(t):
            js[i] = jacobi(b[i], n)
            if math.gcd(b[i], n) > 1:
                comp = True
            elif js[i] == 0 or pow(b[i], (n - 1) // 2, n) != (js[i] % n + n) % n:
                comp = True

    print(*(js))
    print("COMPOSITE" if comp else "PRIME")

if __name__ == '__main__':
    main()
