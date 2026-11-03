import sys

def gray_to_bin(g):
    b = g
    g >>= 1
    while g:
        b ^= g
        g >>= 1
    return b

def fmt_gray(g, n):
    return "".join("1" if (g >> (n - 1 - i)) & 1 else "0" for i in range(n))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "G":
        n = int(tokens[1])
        for i in range(1 << n):
            sys.stdout.write(fmt_gray(i ^ (i >> 1), n) + "\n")
    elif mode == "R":
        g = tokens[1]
        v = int(g, 2)
        sys.stdout.write(str(gray_to_bin(v)) + "\n")
    else:
        n = int(tokens[1])
        r = int(tokens[2])
        sys.stdout.write(fmt_gray(r ^ (r >> 1), n) + "\n")

if __name__ == "__main__":
    main()
