import sys

def largest_histogram_area(heights):
    st = []
    best = 0
    # Append 0 to flush the stack at the end
    hh = heights + [0]
    for i, h in enumerate(hh):
        while st and hh[st[-1]] > h:
            H = hh[st.pop()]
            W = i if not st else i - st[-1] - 1
            area = H * W
            if area > best:
                best = area
        st.append(i)
    return best

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    h = int(tokens[0])
    w = int(tokens[1])
    idx = 2
    g = []
    for _ in range(h):
        g.append([int(x) for x in tokens[idx : idx + w]])
        idx += w

    # Max square
    dp = [[0] * w for _ in range(h)]
    ms = 0
    for r in range(h):
        gr = g[r]
        dpr = dp[r]
        dpr_prev = dp[r - 1] if r > 0 else None
        for c in range(w):
            if gr[c]:
                if r == 0 or c == 0:
                    dpr[c] = 1
                else:
                    dpr[c] = 1 + min(dpr_prev[c], dpr[c - 1], dpr_prev[c - 1])
                if dpr[c] > ms:
                    ms = dpr[c]

    # Max rectangle
    heights = [0] * w
    mr = 0
    for r in range(h):
        gr = g[r]
        for c in range(w):
            heights[c] = heights[c] + 1 if gr[c] else 0
        area = largest_histogram_area(heights)
        if area > mr:
            mr = area

    print(ms * ms)
    print(mr)

if __name__ == '__main__':
    main()
