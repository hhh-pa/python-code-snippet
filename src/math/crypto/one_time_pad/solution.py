import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 2:
        # No output: empty pad of the empty message, or malformed input.
        return
    key = bytes.fromhex(toks[0])
    msg = bytes.fromhex(toks[1])
    sys.stdout.write(bytes(x ^ y for x, y in zip(key, msg)).hex())


if __name__ == "__main__":
    main()
