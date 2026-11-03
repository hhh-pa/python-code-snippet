import sys
import math

def dchar(v):
    if v < 10:
        return chr(ord('0') + v)
    return chr(ord('A') + v - 10)

def to_base(val, b):
    if val == 0:
        return "0"
    digits = []
    while val > 0:
        digits.append(dchar(val % b))
        val //= b
    return "".join(reversed(digits))

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    
    mode = tokens[0]
    if mode == "E":
        n = int(tokens[1])
        p = [int(tokens[2 + i]) for i in range(n)]
        L = []
        rank = 0
        for i in range(n - 1):
            c = sum(1 for j in range(i + 1, n) if p[j] < p[i])
            L.append(c)
            rank += c * math.factorial(n - 1 - i)
        sys.stdout.write(" ".join(map(str, L)) + "\n")
        sys.stdout.write(str(rank) + "\n")
    elif mode == "D":
        n = int(tokens[1])
        L = [int(tokens[2 + i]) for i in range(n - 1)]
        L.append(0)
        avail = list(range(n))
        res = []
        for i in range(n):
            idx = L[i]
            res.append(avail.pop(idx))
        sys.stdout.write(" ".join(map(str, res)) + "\n")
    elif mode == "A":
        b = int(tokens[1])
        X = tokens[2]
        Y = tokens[3]
        v = int(X, b) + int(Y, b)
        sys.stdout.write(to_base(v, b) + "\n")
    else:
        b = int(tokens[1])
        X = tokens[2]
        Y = tokens[3]
        v = int(X, b) * int(Y, b)
        sys.stdout.write(to_base(v, b) + "\n")

if __name__ == "__main__":
    main()
