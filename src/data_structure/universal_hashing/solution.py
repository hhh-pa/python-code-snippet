import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    a = int(tokens[0])
    w = int(tokens[1])
    k = int(tokens[2])
    n = int(tokens[3])
    idx = 4

    mask = (1 << w) - 1 if w > 0 else 0
    shift = w - k
    out = []
    for _ in range(n):
        x = int(tokens[idx])
        idx += 1
        p = (a * x) & mask
        h = p >> shift
        out.append(str(h))

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
