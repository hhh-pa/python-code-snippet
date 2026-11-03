import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    x0 = int(tokens[0])
    M = int(tokens[1])
    cnt = int(tokens[2])

    x = x0
    bits = []
    for _ in range(cnt):
        x = (x * x) % M
        bits.append(str(x & 1))

    print("".join(bits))
    print(x)

if __name__ == '__main__':
    main()
