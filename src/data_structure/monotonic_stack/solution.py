import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n < 0:
        return
    h = [int(tokens[1 + i]) for i in range(n)]

    max_area = 0
    st = []

    for i in range(n + 1):
        cur_h = -1 if i == n else h[i]
        while st and h[st[-1]] >= cur_h:
            height = h[st.pop()]
            width = i if not st else (i - st[-1] - 1)
            area = height * width
            if area > max_area:
                max_area = area
        st.append(i)

    span = [0] * n
    st = []
    for i in range(n):
        while st and h[st[-1]] <= h[i]:
            st.pop()
        span[i] = (i + 1) if not st else (i - st[-1])
        st.append(i)

    sys.stdout.write(f"{max_area}\n")
    sys.stdout.write(" ".join(map(str, span)) + "\n")


if __name__ == "__main__":
    main()
