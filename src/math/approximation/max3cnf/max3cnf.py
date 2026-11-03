import sys

def expected_of(cls, asg):
    tot = 0.0
    for cl in cls:
        sat = False
        open_count = 0
        for lit in cl:
            v = abs(lit)
            if asg[v] >= 0:
                if (lit > 0) == (asg[v] == 1):
                    sat = True
                    break
            else:
                open_count += 1
        if sat:
            tot += 1.0
        elif open_count > 0:
            tot += 1.0 - (0.5 ** open_count)
    return tot

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    m = int(tokens[1])
    idx = 2
    cls = []
    for _ in range(m):
        cls.append([int(tokens[idx]), int(tokens[idx + 1]), int(tokens[idx + 2])])
        idx += 3

    asg = [-1] * (n + 1)
    for v in range(1, n + 1):
        asg[v] = 1
        e1 = expected_of(cls, asg)
        asg[v] = 0
        e0 = expected_of(cls, asg)
        asg[v] = 1 if e1 >= e0 else 0

    sat = 0
    for cl in cls:
        s = False
        for lit in cl:
            if (lit > 0) == (asg[abs(lit)] == 1):
                s = True
                break
        if s:
            sat += 1

    print(*(asg[1 : n + 1]))
    print(sat)

if __name__ == '__main__':
    main()
