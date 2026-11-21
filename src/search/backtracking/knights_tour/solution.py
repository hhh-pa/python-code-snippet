"""Knight's tour via Warnsdorff (ties: smallest row, then column)."""

import sys

MOVES = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n, sr, sc = int(data[0]), int(data[1]), int(data[2])
    seen = [[False] * n for _ in range(n)]
    tour = [(sr, sc)]
    seen[sr][sc] = True

    def onward(r, c):
        return sum(
            1
            for dr, dc in MOVES
            if 0 <= r + dr < n and 0 <= c + dc < n and not seen[r + dr][c + dc]
        )

    while len(tour) < n * n:
        r, c = tour[-1]
        cands = [
            (r + dr, c + dc)
            for dr, dc in MOVES
            if 0 <= r + dr < n and 0 <= c + dc < n and not seen[r + dr][c + dc]
        ]
        if not cands:
            sys.stdout.write("NO TOUR")
            return
        cands.sort(key=lambda p: (onward(*p), p[0], p[1]))
        nr, nc = cands[0]
        seen[nr][nc] = True
        tour.append((nr, nc))
    sys.stdout.write("\n".join(f"{r} {c}" for r, c in tour))


if __name__ == "__main__":
    main()
