# Indexing and ranking (NR 8.4).
import sys


def indexx(arr):
    m = 7
    nstack = 64
    n = len(arr)
    istack = [0] * nstack
    indx = list(range(n))
    ir = n - 1
    jstack = -1
    l = 0
    while True:
        if ir - l < m:
            j = l + 1
            while j <= ir:
                indxt = indx[j]
                a = arr[indxt]
                i = j - 1
                while i >= l:
                    if arr[indx[i]] <= a:
                        break
                    indx[i + 1] = indx[i]
                    i -= 1
                indx[i + 1] = indxt
                j += 1
            if jstack < 0:
                break
            ir = istack[jstack]
            jstack -= 1
            l = istack[jstack]
            jstack -= 1
        else:
            k = (l + ir) >> 1
            indx[k], indx[l + 1] = indx[l + 1], indx[k]
            if arr[indx[l]] > arr[indx[ir]]:
                indx[l], indx[ir] = indx[ir], indx[l]
            if arr[indx[l + 1]] > arr[indx[ir]]:
                indx[l + 1], indx[ir] = indx[ir], indx[l + 1]
            if arr[indx[l]] > arr[indx[l + 1]]:
                indx[l], indx[l + 1] = indx[l + 1], indx[l]
            i = l + 1
            j = ir
            indxt = indx[l + 1]
            a = arr[indxt]
            while True:
                while True:
                    i += 1
                    if not arr[indx[i]] < a:
                        break
                while True:
                    j -= 1
                    if not arr[indx[j]] > a:
                        break
                if j < i:
                    break
                indx[i], indx[j] = indx[j], indx[i]
            indx[l + 1] = indx[j]
            indx[j] = indxt
            jstack += 2
            if ir - i + 1 >= j - l:
                istack[jstack] = ir
                istack[jstack - 1] = i
                ir = j - 1
            else:
                istack[jstack] = j - 1
                istack[jstack - 1] = l
                l = i
    return indx


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    op = toks[0]
    if op != "INDEX" and op != "RANK":
        return
    n = int(toks[1])
    arr = [int(w) for w in toks[2:2 + n]]
    indx = indexx(arr)
    if op == "INDEX":
        out = indx
    else:
        out = [0] * n
        for j in range(n):
            out[indx[j]] = j
    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
