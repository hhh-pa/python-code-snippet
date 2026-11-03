import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    p = list(range(n))
    d = [-1] * n
    
    out = [" ".join(map(str, p))]
    while True:
        mob = -1
        mobpos = -1
        for i in range(n):
            v = p[i]
            j = i + d[v]
            if 0 <= j < n and p[j] < v and v > mob:
                mob = v
                mobpos = i
        if mob < 0:
            break
        j = mobpos + d[mob]
        p[mobpos], p[j] = p[j], p[mobpos]
        for v in range(mob + 1, n):
            d[v] = -d[v]
        out.append(" ".join(map(str, p)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
