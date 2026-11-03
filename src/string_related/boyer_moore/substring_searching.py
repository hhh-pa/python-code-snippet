import sys

def boyer_moore(text, pattern):
    N = len(text)
    M = len(pattern)
    if M == 0:
        return True
    if M > N:
        return False

    right = [-1] * 256
    for j, ch in enumerate(pattern):
        right[ord(ch)] = j

    i = 0
    while i <= N - M:
        skip = 0
        for j in range(M - 1, -1, -1):
            if pattern[j] != text[i + j]:
                skip = j - right[ord(text[i + j])]
                if skip < 1:
                    skip = 1
                break
        if skip == 0:
            return True
        i += skip
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
        if boyer_moore(text, pattern):
            out.append("YES")
        else:
            out.append("NO")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
