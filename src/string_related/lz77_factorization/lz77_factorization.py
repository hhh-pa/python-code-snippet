import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    n = len(s)
    i = 0
    out = []

    while i < n:
        best_len = 0
        best_off = 0
        for j in range(i):
            length = 0
            while i + length < n and j + length < n and s[j + length] == s[i + length]:
                length += 1
            if length > best_len:
                best_len = length
                best_off = i - j

        if best_len == 0:
            out.append(f"0 0 {s[i]}")
            i += 1
        else:
            nxt = s[i + best_len] if i + best_len < n else '$'
            out.append(f"{best_off} {best_len} {nxt}")
            i += best_len + (1 if i + best_len < n else 0)
            if best_len > 0 and i >= n:
                break

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
