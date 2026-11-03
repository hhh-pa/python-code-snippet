import sys
import bisect

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
    
    a = [int(next(it)) for _ in range(n)]
    key = int(next(it))
    
    lb = bisect.bisect_left(a, key)
    ub = bisect.bisect_right(a, key)
    
    if lb >= len(a) or a[lb] != key:
        print("-1 -1 0")
    else:
        print(f"{lb} {ub - 1} {ub - lb}")

if __name__ == "__main__":
    main()
