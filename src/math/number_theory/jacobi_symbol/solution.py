import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    a, n = int(toks[0]), int(toks[1])
    a %= n
    # Quadratic reciprocity loop (values stay below 2^63).
    t = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a %= n
    sys.stdout.write(str(t if n == 1 else 0))


if __name__ == "__main__":
    main()
