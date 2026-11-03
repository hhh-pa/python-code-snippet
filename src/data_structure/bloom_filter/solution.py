import sys

MASK64 = 0xFFFFFFFFFFFFFFFF
C1 = 0x9E3779B97F4A7C15
C2 = 0xBF58476D1CE4E5B9


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    k = int(tokens[1])
    n = int(tokens[2])
    q = int(tokens[3])
    idx = 4

    bits = bytearray(m)

    def add(ux):
        h1 = (ux * C1) & MASK64
        h2 = (((ux * C2) & MASK64) + 1) | 1
        for i in range(k):
            pos = (h1 + i * h2) % m
            bits[pos] = 1

    def query(ux):
        h1 = (ux * C1) & MASK64
        h2 = (((ux * C2) & MASK64) + 1) | 1
        for i in range(k):
            pos = (h1 + i * h2) % m
            if not bits[pos]:
                return False
        return True

    for _ in range(n):
        x = int(tokens[idx])
        idx += 1
        add(x & MASK64)

    out = []
    for _ in range(q):
        x = int(tokens[idx])
        idx += 1
        out.append("YES" if query(x & MASK64) else "NO")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
