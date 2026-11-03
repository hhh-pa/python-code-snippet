import sys

def npow2inv(n):
    x = 1.0
    for _ in range(200):
        p = 1.0
        for _ in range(n - 1):
            p *= x
        f = p * x - 2.0
        d = float(n) * p
        x -= f / d
    return x

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
    except StopIteration:
        return

    u = 0.0
    for _ in range(n):
        c = float(next(it))
        t = float(next(it))
        u += c / t

    bound = float(n) * (npow2inv(n) - 1.0)
    print("RMS YES" if u <= bound else "RMS NO")
    print("EDF YES" if u <= 1.0 else "EDF NO")

if __name__ == "__main__":
    main()
