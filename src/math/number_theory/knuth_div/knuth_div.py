import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    A = int(tokens[0])
    B = int(tokens[1])
    print(A // B)
    print(A % B)

if __name__ == '__main__':
    main()
