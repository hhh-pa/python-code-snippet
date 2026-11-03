import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "P":
        n = int(tokens[1])
        p = [int(tokens[2 + i]) for i in range(n)]
        i = n - 2
        while i >= 0 and p[i] >= p[i+1]:
            i -= 1
        if i < 0:
            sys.stdout.write("NONE\n")
            return
        j = n - 1
        while p[j] <= p[i]:
            j -= 1
        p[i], p[j] = p[j], p[i]
        p[i+1:] = reversed(p[i+1:])
        sys.stdout.write(" ".join(map(str, p)) + "\n")
    else:
        n = int(tokens[1])
        r = int(tokens[2])
        c = [int(tokens[3 + i]) for i in range(r)]
        i = r - 1
        while i >= 0 and c[i] == n - r + i:
            i -= 1
        if i < 0:
            sys.stdout.write("NONE\n")
            return
        c[i] += 1
        for j in range(i + 1, r):
            c[j] = c[j-1] + 1
        sys.stdout.write(" ".join(map(str, c)) + "\n")

if __name__ == "__main__":
    main()
