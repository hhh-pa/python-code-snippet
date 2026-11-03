import sys

def phi(n):
    r = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            r -= r // p
        p += 1
    if x > 1:
        r -= r // x
    return r

def ipow(b, e):
    return b ** e

def necklaces(n, k):
    s = 0
    for d in range(1, n + 1):
        if n % d == 0:
            s += phi(d) * (k ** (n // d))
    return s // n

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    n = int(tokens[1])
    k = int(tokens[2])
    
    N = necklaces(n, k)
    if mode == "N":
        sys.stdout.write(str(N) + "\n")
    elif n % 2 == 1:
        ans = (N + (k ** ((n + 1) // 2))) // 2
        sys.stdout.write(str(ans) + "\n")
    else:
        ans = (2 * N + (k ** (n // 2 + 1)) + (k ** (n // 2))) // 4
        sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
