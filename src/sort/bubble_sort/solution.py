import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    print(" ".join(str(x) for x in a))
    print(swaps)

if __name__ == "__main__":
    main()
