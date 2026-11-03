import sys

sys.setrecursionlimit(200000)

def char_at(s, d):
    return ord(s[d]) if d < len(s) else -1

def sort3str(a, lo, hi, d):
    if hi <= lo:
        return
    v = char_at(a[lo], d)
    lt = lo
    gt = hi
    i = lo + 1
    while i <= gt:
        t = char_at(a[i], d)
        if t < v:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif t > v:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    sort3str(a, lo, lt - 1, d)
    if v >= 0:
        sort3str(a, lt, gt, d + 1)
    sort3str(a, gt + 1, hi, d)

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n = int(lines[0].strip())
    a = lines[1 : 1 + n]
    if len(a) > 0:
        sort3str(a, 0, len(a) - 1, 0)
    sys.stdout.write("[" + ",".join(a) + "]")

if __name__ == "__main__":
    main()
