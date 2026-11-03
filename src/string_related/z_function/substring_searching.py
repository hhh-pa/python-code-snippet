import sys

def z_function(text, pattern):
    m = len(pattern)
    if m == 0:
        return True
    s = pattern + "$" + text
    n = len(s)
    z = [0] * n
    l = 0
    r = 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
        if z[i] == m:
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
        if z_function(text, pattern):
            out.append("YES")
        else:
            out.append("NO")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
