import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    T = int(tokens[0])
    idx = 1
    out = []
    for _ in range(T):
        sg = tokens[idx]
        bs = tokens[idx + 1]
        idx += 2
        v = 0
        for ch in bs:
            v = v * 2 + (1 if ch == '1' else 0)
        if sg == "-":
            v = -v
        out.append(f"ATTR {v}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
