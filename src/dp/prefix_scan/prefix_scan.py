import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[1 + i]) for i in range(n)]

    N = 1
    while N < n:
        N *= 2

    t = [0] * N
    for i in range(n):
        t[i] = a[i]

    # Up-sweep (reduce)
    d = 1
    while d < N:
        step = 2 * d
        for k in range(0, N, step):
            t[k + step - 1] += t[k + d - 1]
        d = step

    t[N - 1] = 0

    # Down-sweep
    d = N // 2
    while d >= 1:
        step = 2 * d
        for k in range(0, N, step):
            tmp = t[k + d - 1]
            t[k + d - 1] = t[k + step - 1]
            t[k + step - 1] += tmp
        d //= 2

    exclusive = [str(t[i]) for i in range(n)]
    inclusive = [str(t[i] + a[i]) for i in range(n)]
    sys.stdout.write(" ".join(exclusive) + "\n")
    sys.stdout.write(" ".join(inclusive) + "\n")

if __name__ == '__main__':
    main()
