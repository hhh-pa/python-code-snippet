import sys

R = 256

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a = int(tokens[0])
    b = int(tokens[1])
    m = int(tokens[2])

    minv = 1
    for x in range(1, R):
        if (m * x) % R == 1:
            minv = x
            break

    mp = (R - minv) % R

    def redc(T):
        q = ((T & 255) * mp) & 255
        t = (T + q * m) >> 8
        if t >= m:
            t -= m
        return t

    aM = ((a % m) * R) % m
    bM = ((b % m) * R) % m
    abM = redc(aM * bM)
    ab = redc(abM)

    print(f"{aM} {bM}")
    print(abM)
    print(ab)

if __name__ == '__main__':
    main()
