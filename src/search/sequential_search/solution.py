import sys


def main():
    data = list(map(int, sys.stdin.read().split()))
    if len(data) < 2 or data[0] < 0:
        return
    n = data[0]
    if len(data) < 2 + n:
        return
    target = data[1 + n]
    ans = -1
    for i in range(n):
        if data[1 + i] == target:
            ans = i
            break
    print(ans)


if __name__ == "__main__":
    main()
