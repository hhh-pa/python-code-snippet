import sys

def modpow(b, e, m):
    if m == 1:
        return 0
    return pow(b, e, m)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    vals = [int(x) for x in tokens]
    cnt = len(vals)
    if cnt == 3:
        print(modpow(vals[0], vals[1], vals[2]))
        return

    t = vals[0]
    out = []
    if t > 0 and cnt == 3 * t + 1:
        for i in range(t):
            out.append(str(modpow(vals[1 + 3 * i], vals[1 + 3 * i + 1], vals[1 + 3 * i + 2])))
    else:
        out.append(str(modpow(vals[0], vals[1], vals[2])))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
