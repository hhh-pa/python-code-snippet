import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    n = len(s)
    i = 0
    res = []
    while i < n:
        c = s[i]
        cnt = 1
        while i + cnt < n and s[i + cnt] == c:
            cnt += 1
        res.append(f"{c}{cnt}")
        i += cnt
    print(" ".join(res))

if __name__ == "__main__":
    main()
