import sys
from collections import deque

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        n_str = next(it)
    except StopIteration:
        return
    n = int(n_str)
    
    vals = [int(next(it)) for _ in range(n)]
    if n == 0 or vals[0] == -1:
        print(0)
        return
        
    q = deque([(0, 1)])
    while q:
        idx, d = q.popleft()
        if vals[idx] == -1:
            continue
        l = 2 * idx + 1
        r = 2 * idx + 2
        left_exists = l < n and vals[l] != -1
        right_exists = r < n and vals[r] != -1
        if not left_exists and not right_exists:
            print(d)
            return
        if l < n:
            q.append((l, d + 1))
        if r < n:
            q.append((r, d + 1))
            
    print(0)

if __name__ == "__main__":
    main()
