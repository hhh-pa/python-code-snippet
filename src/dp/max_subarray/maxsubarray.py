import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    T = int(tokens[0])
    idx = 1
    out = []
    for _ in range(T):
        N = int(tokens[idx])
        idx += 1
        A = [int(x) for x in tokens[idx : idx + N]]
        idx += N

        # Max non-contiguous (max2)
        # If all negative, max element.
        # Otherwise, sum of positive elements.
        max_elem = max(A)
        if max_elem <= 0:
            max1 = max_elem
            max2 = max_elem
        else:
            max2 = sum(x for x in A if x > 0)
            # Kadane's algorithm for max contiguous (max1)
            cur = 0
            max1 = 0
            for x in A:
                cur += x
                if cur < 0:
                    cur = 0
                elif cur > max1:
                    max1 = cur
        out.append(f"{max1} {max2}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
