import sys

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
    k = int(next(it))
    
    arr = [int(next(it)) for _ in range(n)]
    arr.sort()
    
    count = 0
    i = 0
    j = 1
    while j < n:
        diff = arr[j] - arr[i]
        if diff == k:
            count += 1
            j += 1
        elif diff < k:
            j += 1
        else:
            i += 1
            if i == j:
                j += 1
                
    print(count)

if __name__ == "__main__":
    main()
