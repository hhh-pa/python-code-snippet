import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    d = [0] * n
    w = [0] * n
    mx = 0
    idx = 1
    for i in range(n):
        d[i] = int(tokens[idx])
        w[i] = int(tokens[idx + 1])
        idx += 2
        if d[i] > mx:
            mx = d[i]
            
    order = list(range(n))
    order.sort(key=lambda i: (-w[i], i))
    
    slot = [-1] * (mx + 1)
    ins = [False] * n
    
    for i in order:
        t = min(d[i], mx)
        while t >= 1 and slot[t] != -1:
            t -= 1
        if t >= 1:
            slot[t] = i
            ins[i] = True
            
    pen = 0
    sel = []
    for i in range(n):
        if ins[i]:
            sel.append(i)
        else:
            pen += w[i]
            
    print(pen)
    print(*(sel))

if __name__ == '__main__':
    main()
