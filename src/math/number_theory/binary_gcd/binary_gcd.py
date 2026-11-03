import sys

def bgcd(a, b):
    if a == 0:
        return abs(b)
    if b == 0:
        return abs(a)
    a, b = abs(a), abs(b)
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1
    while (a & 1) == 0:
        a >>= 1
    while b != 0:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b = b - a
    return a << shift

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    vals = [int(x) for x in tokens]
    cnt = len(vals)
    if cnt == 2:
        print(bgcd(vals[0], vals[1]))
        return

    t = vals[0]
    out = []
    if t > 0 and cnt == 2 * t + 1:
        for i in range(t):
            out.append(str(bgcd(vals[1 + 2 * i], vals[1 + 2 * i + 1])))
    else:
        for i in range(0, cnt - 1, 2):
            out.append(str(bgcd(vals[i], vals[i + 1])))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
