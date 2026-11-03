import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    T = int(tokens[1])
    eta = float(tokens[2])
    idx = 3
    w = [1.0] * n
    for _ in range(T):
        for i in range(n):
            g = float(tokens[idx])
            idx += 1
            w[i] *= 1.0 + eta * g

    s = sum(w)
    out = [f"{(wi / s) + 0.0:.6f}" for wi in w]
    print(" ".join(out))

if __name__ == '__main__':
    main()
