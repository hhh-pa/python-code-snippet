import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]

    t = "^#" + "#".join(s) + "#$"
    m = len(t)
    p = [0] * m
    c = 0
    r = 0

    for i in range(1, m - 1):
        i_mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[i_mirror])

        while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
            p[i] += 1

        if i + p[i] > r:
            c = i
            r = i + p[i]

    max_len = 0
    center_idx = 0
    total_palindromes = 0

    for i in range(1, m - 1):
        if p[i] > max_len:
            max_len = p[i]
            center_idx = i
        total_palindromes += (p[i] + 1) // 2

    start_pos = (center_idx - max_len) // 2
    longest_pal = s[start_pos:start_pos + max_len]

    print(max_len)
    print(longest_pal)
    print(total_palindromes)

if __name__ == "__main__":
    main()
