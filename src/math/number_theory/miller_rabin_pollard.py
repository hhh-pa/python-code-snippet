import math
import random
import sys

def mod_pow(base, exp, m):
    return pow(base, exp, m)

def gcd(a, b):
    return math.gcd(a, b)

def miller_rabin(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    s = 0
    while (d & 1) == 0:
        d >>= 1
        s += 1

    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n <= a:
            break
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(1, s):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    x = 2
    y = 2
    d = 1
    c = 1

    def f(val):
        return (val * val + c) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        diff = abs(x - y)
        d = gcd(diff, n)
        if d == n:
            x = 2
            y = 2
            c += 1
            d = 1
    return d

def factorize(n, factors):
    if n == 1:
        return
    if miller_rabin(n):
        factors.append(n)
        return
    d = pollard_rho(n)
    factorize(d, factors)
    factorize(n // d, factors)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    t = int(tokens[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(tokens[idx])
        idx += 1
        if miller_rabin(n):
            out.append("PRIME")
        else:
            factors = []
            factorize(n, factors)
            factors.sort()
            out.append("COMPOSITE " + " ".join(map(str, factors)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
