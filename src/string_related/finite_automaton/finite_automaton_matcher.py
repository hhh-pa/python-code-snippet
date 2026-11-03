import sys

def compute_transition_function(pattern):
    m = len(pattern)
    delta = [[0] * 26 for _ in range(m + 1)]
    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    for q in range(m + 1):
        for c in range(26):
            ch = chr(ord('a') + c)
            if q < m and pattern[q] == ch:
                delta[q][c] = q + 1
            elif q == 0:
                delta[q][c] = 0
            else:
                delta[q][c] = delta[pi[q - 1]][c]

    return delta

def finite_automaton_matcher(pattern, text):
    m = len(pattern)
    n = len(text)
    delta = compute_transition_function(pattern)
    matches = []
    q = 0
    for i in range(n):
        c = ord(text[i]) - ord('a')
        q = delta[q][c]
        if q == m:
            matches.append(i + 1 - m)
    return matches

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    num_q = int(next(it))
    out = []
    for _ in range(num_q):
        pattern = next(it)
        text = next(it)
        matches = finite_automaton_matcher(pattern, text)
        if not matches:
            out.append("-1")
        else:
            out.append(" ".join(str(x) for x in matches))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
