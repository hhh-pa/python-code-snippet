import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]

    d = {chr(i): i for i in range(256)}
    nxt = 256
    w = ""
    codes = []

    for c in s:
        wc = w + c
        if wc in d:
            w = wc
        else:
            codes.append(d[w])
            d[wc] = nxt
            nxt += 1
            w = c

    if w:
        codes.append(d[w])

    print(" ".join(str(x) for x in codes))

if __name__ == "__main__":
    main()
