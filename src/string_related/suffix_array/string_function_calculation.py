import sys

def cal_suffix_array(t):
    n = len(t)
    k = 1
    sa = list(range(n))
    rank = [ord(c) - 97 for c in t]
    tmp = [0] * n

    while k < n:
        shift = 20
        keys = [(rank[x] << shift) | (rank[x + k] + 1 if x + k < n else 0) for x in range(n)]
        sa.sort(key=keys.__getitem__)
        curr_rank = 0
        tmp[sa[0]] = 0
        prev_k = keys[sa[0]]
        for i in range(1, n):
            cur_k = keys[sa[i]]
            if cur_k != prev_k:
                curr_rank += 1
                prev_k = cur_k
            tmp[sa[i]] = curr_rank
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2

    return sa

def kasai(s, sa):
    n = len(s)
    lcp = [0] * n
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return lcp

def max_value(t):
    n = len(t)
    if n == 0:
        return 0
    suffix_array = cal_suffix_array(t)
    lcp = kasai(t, suffix_array)

    ans = n

    prev_less = [-1] * n
    stack = []
    for i in range(n):
        while stack and lcp[stack[-1]] >= lcp[i]:
            stack.pop()
        prev_less[i] = stack[-1] if stack else -1
        stack.append(i)

    next_less = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and lcp[stack[-1]] >= lcp[i]:
            stack.pop()
        next_less[i] = stack[-1] if stack else n
        stack.append(i)

    for i in range(n):
        cnt = next_less[i] - prev_less[i]
        val = cnt * lcp[i]
        if val > ans:
            ans = val

    return ans

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    s = tokens[0]
    print(max_value(s))

if __name__ == "__main__":
    main()
