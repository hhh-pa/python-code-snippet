import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    G = tokens[0]
    M = tokens[1]
    r = len(G) - 1
    d = [1 if c == '1' else 0 for c in M] + [0] * r
    g_bits = [1 if c == '1' else 0 for c in G]
    for i in range(len(M)):
        if d[i] == 1:
            for j in range(len(G)):
                d[i + j] ^= g_bits[j]
    print("".join(str(d[i]) for i in range(len(M), len(d))))

if __name__ == "__main__":
    main()
