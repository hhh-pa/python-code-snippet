import sys
from collections import Counter

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    t = int(next(it))
    out = []

    for _ in range(t):
        s = next(it)
        n = len(s)
        counts = Counter()
        for i in range(n):
            for j in range(i + 1, n + 1):
                sorted_sub = "".join(sorted(s[i:j]))
                counts[sorted_sub] += 1

        ans = sum(c * (c - 1) // 2 for c in counts.values())
        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
