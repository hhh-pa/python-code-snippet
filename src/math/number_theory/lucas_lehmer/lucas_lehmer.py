import sys

def ll_prime(p):
    if p == 2:
        return True
    M = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % M
    return s == 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    out = []
    for token in tokens:
        p = int(token)
        out.append("PRIME" if ll_prime(p) else "COMPOSITE")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
