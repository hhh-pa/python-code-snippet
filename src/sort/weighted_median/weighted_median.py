import sys

def weighted_median(vals, wts):
    n = len(vals)
    if n == 0:
        return 0
    v = list(vals)
    w = list(wts)
    w_left = 0.0
    l, r = 0, n - 1
    while l < r:
        tmp = sorted(v[l : r + 1])
        pivot = tmp[(r - l) // 2]
        
        less_v, less_w = [], []
        eq_v, eq_w = [], []
        gt_v, gt_w = [], []
        
        for i in range(l, r + 1):
            if v[i] < pivot:
                less_v.append(v[i])
                less_w.append(w[i])
            elif v[i] == pivot:
                eq_v.append(v[i])
                eq_w.append(w[i])
            else:
                gt_v.append(v[i])
                gt_w.append(w[i])
                
        w_less = sum(less_w)
        w_eq = sum(eq_w)
        
        nv = less_v + eq_v + gt_v
        nw = less_w + eq_w + gt_w
        for i in range(len(nv)):
            v[l + i] = nv[i]
            w[l + i] = nw[i]
            
        eq_start = l + len(less_v)
        eq_end = eq_start + len(eq_v) - 1
        
        if w_left + w_less < 0.5 and w_left + w_less + w_eq >= 0.5:
            return pivot
        if w_left + w_less >= 0.5:
            r = eq_start - 1
        else:
            w_left += w_less + w_eq
            l = eq_end + 1
            
    return v[l]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 0:
        print(0)
        return
    vals = [int(tokens[1 + i]) for i in range(n)]
    wts = [float(tokens[1 + n + i]) for i in range(n)]
    print(weighted_median(vals, wts))

if __name__ == "__main__":
    main()
