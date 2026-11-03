import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    x = int(tokens[0])
    m = int(tokens[1])
    mu = (1 << 32) // m
    q = (x * mu) >> 32
    r = x - q * m
    while r < 0:
        r += m
        q -= 1
    while r >= m:
        r -= m
        q += 1
    print(f"{q} {r}")

if __name__ == '__main__':
    main()
