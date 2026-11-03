import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    s = [0] * n
    f = [0] * n
    idx = 1
    for i in range(n):
        s[i] = int(tokens[idx])
        f[i] = int(tokens[idx + 1])
        idx += 2
        
    order = list(range(n))
    order.sort(key=lambda i: (f[i], s[i], i))
    
    sel = []
    last = -1
    first = True
    for j in order:
        if first or s[j] >= last:
            sel.append(j)
            last = f[j]
            first = False
            
    print(len(sel))
    print(*(sel))

if __name__ == '__main__':
    main()
