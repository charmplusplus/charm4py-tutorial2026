import random
import math
from charm4py import charm, Chare, Future, coro

MAX_INT = 10**13
SIEVE_LIMIT = 10**6


def _build_sieve(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray((limit - i * i) // i + 1)
    return [i for i, v in enumerate(sieve) if v]


SMALL_PRIMES = _build_sieve(SIEVE_LIMIT)


def _is_prime(n):
    if n < 2:
        return False
    sqrt_n = math.isqrt(n)
    for p in SMALL_PRIMES:
        if p > sqrt_n:
            return True
        if n % p == 0:
            return n == p
    # Extended 6k±1 trial division for n > SIEVE_LIMIT^2
    i = (SIEVE_LIMIT // 6 + 1) * 6 - 1
    while i <= sqrt_n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


class Worker(Chare):

    def checkPrimality(self, numbers, future):
        results = {n: _is_prime(n) for n in numbers}
        future.send(results)


@coro
def main(args):
    if len(args) < 3:
        print("Usage: charmrun ++local +pN primes.py K N [--print]")
        charm.exit()

    K = int(args[1])
    N = int(args[2])
    print_results = "--print" in args

    numbers = [random.randint(0, MAX_INT) for _ in range(K)]

    chunks = [numbers[i::N] for i in range(N)]
    futures = [Future() for _ in range(N)]
    workers = [Chare(Worker) for _ in range(N)]
    for i in range(N):
        workers[i].checkPrimality(chunks[i], futures[i])

    primality = {}
    for f in charm.iwait(futures):
        primality.update(f.get())

    prime_count = sum(primality.values())
    print(f"Tested {K} numbers: {prime_count} primes, {K - prime_count} composites.")
    if print_results:
        for n, is_prime in primality.items():
            print(f"  {n}: {'prime' if is_prime else 'composite'}")
    charm.exit()


charm.start(main)
