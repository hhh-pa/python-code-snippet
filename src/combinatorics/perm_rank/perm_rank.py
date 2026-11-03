import sys
import math

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "R":
        n = int(tokens[1])
        p = [int(tokens[2 + i]) for i in range(n)]
        L = [0] * n
        rank = 0
        for i in range(n):
            cnt = sum(1 for j in range(i + 1, n) if p[j] < p[i])
            L[i] = cnt
            rank += cnt * math.factorial(n - 1 - i)
        sys.stdout.write(f"{rank}\n")
        sys.stdout.write(" ".join(map(str, L)) + "\n")
    else:
        n = int(tokens[1])
        r = int(tokens[2])
        avail = list(range(n))
        p = []
        for i in range(n):
            f = math.factorial(n - 1 - i)
            idx = r // f
            r %= f
            p.append(avail.pop(idx))
        sys.stdout.write(" ".join(map(str, p)) + "\n")

if __name__ == "__main__":
    main()
