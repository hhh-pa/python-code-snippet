import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    idx = 1
    boxes = []
    for _ in range(n):
        x = int(tokens[idx])
        y = int(tokens[idx + 1])
        z = int(tokens[idx + 2])
        idx += 3
        for q in [(x, y, z), (x, z, y), (y, z, x)]:
            a, b, h = q[0], q[1], q[2]
            if a < b:
                a, b = b, a
            boxes.append((a, b, h))
            
    boxes.sort(key=lambda b: (b[0] * b[1], b[0], b[1]), reverse=True)
    m = len(boxes)
    dp = [b[2] for b in boxes]
    for i in range(m):
        for j in range(i):
            if boxes[j][0] > boxes[i][0] and boxes[j][1] > boxes[i][1]:
                if dp[j] + boxes[i][2] > dp[i]:
                    dp[i] = dp[j] + boxes[i][2]
    ans = max(dp) if dp else 0
    print(ans)

if __name__ == '__main__':
    main()
