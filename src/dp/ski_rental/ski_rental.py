import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    B = int(tokens[0])
    T = int(tokens[1])

    off = min(T, B)
    det = T if T < B else (B - 1) + B
    if T >= B:
        rnd = B * B + B * (B - 1) // 2
    else:
        rnd = T * (T - 1) // 2 + T * (2 * B - T)

    print(off)
    print(det)
    print(rnd)

if __name__ == '__main__':
    main()
