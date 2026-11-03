import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    n = len(s)
    reps = []

    for i in range(n):
        for length in range(1, (n - i) // 2 + 1):
            if s[i:i + length] == s[i + length:i + 2 * length]:
                reps.append(f"{i} {length}")

    out = [str(len(reps))]
    out.extend(reps)
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
