import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n < 2:
        print("0\n")
        return

    is_prime = bytearray(b"\x01") * (n + 1)
    is_prime[0] = 0
    is_prime[1] = 0

    i = 2
    while i * i <= n:
        if is_prime[i]:
            is_prime[i * i : n + 1 : i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1

    primes = [str(i) for i in range(2, n + 1) if is_prime[i]]
    print(len(primes))
    print(" ".join(primes))

if __name__ == '__main__':
    main()
