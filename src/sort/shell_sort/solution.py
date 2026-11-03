import sys

def shell_sort(a):
    gap = len(a) // 2
    while gap > 0:
        for i in range(gap, len(a)):
            tmp = a[i]
            j = i
            while j >= gap and a[j - gap] > tmp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = tmp
        gap //= 2

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = [int(tokens[i]) for i in range(1, 1 + n)]
    shell_sort(nums)
    sys.stdout.write("[" + ",".join(str(x) for x in nums) + "]")

if __name__ == "__main__":
    main()
