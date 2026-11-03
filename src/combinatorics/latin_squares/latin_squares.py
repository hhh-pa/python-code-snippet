import sys

def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 6:
        sys.stdout.write("NONE\n")
        return
    if is_prime(n):
        for i in range(n):
            sys.stdout.write(" ".join(str((i + j) % n) for j in range(n)) + "\n")
        for i in range(n):
            sys.stdout.write(" ".join(str((i + 2 * j) % n) for j in range(n)) + "\n")
        sys.stdout.write("ORTHOGONAL\n")
    else:
        for i in range(n):
            sys.stdout.write(" ".join(str((i + j) % n) for j in range(n)) + "\n")
        sys.stdout.write("NO_PAIR\n")

if __name__ == "__main__":
    main()
