"""Tower of Hanoi move sequence (A -> C via B)."""

import sys

sys.setrecursionlimit(10000)


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    moves = []

    def hanoi(k, src, dst, aux):
        if k == 0:
            return
        hanoi(k - 1, src, aux, dst)
        moves.append(f"{src} {dst}")
        hanoi(k - 1, aux, dst, src)

    hanoi(n, "A", "C", "B")
    sys.stdout.write(str(len(moves)) + "\n" + "\n".join(moves))


if __name__ == "__main__":
    main()
