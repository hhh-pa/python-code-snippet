import sys

def selection_sort(a):
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    selection_sort(a)
    sys.stdout.write(" ".join(str(x) for x in a) + "\n")

if __name__ == "__main__":
    main()
