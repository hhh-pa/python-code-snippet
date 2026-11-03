import sys

def kmp(text, pattern):
    if not pattern:
        return True
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    j = 0
    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == m:
            return True
    return False

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    out = []
    for _ in range(n):
        text = next(it)
        pattern = next(it)
        if kmp(text, pattern):
            out.append("YES")
        else:
            out.append("NO")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
