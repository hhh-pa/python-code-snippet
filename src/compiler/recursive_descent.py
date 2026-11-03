import sys

sys.setrecursionlimit(200000)

def solve(s):
    p = 0
    err = False

    def parseF():
        nonlocal p, err
        if err or p >= len(s):
            err = True
            return 0
        if s[p] == '(':
            p += 1
            v = parseE()
            if err or p >= len(s) or s[p] != ')':
                err = True
                return 0
            p += 1
            return v
        if s[p] == '-':
            p += 1
            return -parseF()
        if not ('0' <= s[p] <= '9'):
            err = True
            return 0
        v = 0
        while p < len(s) and ('0' <= s[p] <= '9'):
            v = v * 10 + (ord(s[p]) - ord('0'))
            p += 1
        return v

    def parseT():
        nonlocal p, err
        v = parseF()
        while not err and p < len(s) and s[p] in ('*', '/'):
            op = s[p]
            p += 1
            r = parseF()
            if err:
                return 0
            if op == '*':
                v = v * r
            else:
                if r == 0:
                    err = True
                    return 0
                sign = -1 if (v < 0) ^ (r < 0) else 1
                v = sign * (abs(v) // abs(r))
        return v

    def parseE():
        nonlocal p, err
        v = parseT()
        while not err and p < len(s) and s[p] in ('+', '-'):
            op = s[p]
            p += 1
            r = parseT()
            if err:
                return 0
            if op == '+':
                v = v + r
            else:
                v = v - r
        return v

    val = parseE()
    if err or p != len(s):
        return "RD ERROR"
    return f"RD {val}"

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    T = int(tokens[0])
    out = []
    for i in range(1, T + 1):
        if i < len(tokens):
            out.append(solve(tokens[i]))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
