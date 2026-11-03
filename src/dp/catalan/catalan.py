import sys

def cat(k):
    C = [0] * (k + 1)
    C[0] = 1
    for i in range(1, k + 1):
        s = 0
        for j in range(i):
            s += C[j] * C[i - 1 - j]
        C[i] = s
    return C[k]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    print(cat(n))
    print(cat(m - 2) if m >= 2 else 0)

if __name__ == '__main__':
    main()
