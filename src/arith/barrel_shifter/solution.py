import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    data, hot = toks[0], toks[1]
    n = len(data)
    # One-hot select: exactly one control line high; its index from
    # the right is the shift amount. Single mux pass, MSB replicated.
    k = hot[::-1].index("1")
    sign = data[0]
    out = [data[i - k] if i - k >= 0 else sign for i in range(n)]
    sys.stdout.write("".join(out))


if __name__ == "__main__":
    main()
