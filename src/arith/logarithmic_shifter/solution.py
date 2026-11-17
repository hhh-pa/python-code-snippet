import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        return
    data, amt = toks[0], toks[1]
    n = len(data)
    # One stage per amount bit: stage j shifts by 2**j or passes.
    cur = [ord(c) - 48 for c in data]
    for j in range(len(amt)):
        if amt[len(amt) - 1 - j] == "1":
            step = 1 << j
            sign = cur[0]
            cur = [cur[i - step] if i - step >= 0 else sign for i in range(n)]
    sys.stdout.write("".join(chr(48 + b) for b in cur))


if __name__ == "__main__":
    main()
