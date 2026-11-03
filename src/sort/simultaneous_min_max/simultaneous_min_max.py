import sys

def simultaneous_min_max(a):
    n = len(a)
    if n == 0:
        return 0, 0
    if n == 1:
        return a[0], a[0]
    if n % 2 == 0:
        if a[0] < a[1]:
            mn, mx = a[0], a[1]
        else:
            mn, mx = a[1], a[0]
        i = 2
    else:
        mn = mx = a[0]
        i = 1
    while i + 1 < n:
        if a[i] < a[i + 1]:
            sm, lg = a[i], a[i + 1]
        else:
            sm, lg = a[i + 1], a[i]
        if sm < mn:
            mn = sm
        if lg > mx:
            mx = lg
        i += 2
    return mn, mx

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n == 0:
        print("0 0")
        return
    a = [int(tokens[i]) for i in range(1, 1 + n)]
    mn, mx = simultaneous_min_max(a)
    print(f"{mn} {mx}")

if __name__ == "__main__":
    main()
