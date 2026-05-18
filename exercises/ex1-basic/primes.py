import random
from charm4py import charm, Chare, Future, coro

MAX_INT = 10**13


class Worker(Chare):

    def checkPrimality(self, numbers, future):
        # TODO: Test primality of each number in `numbers` using _is_prime,
        # store results in a dict mapping each number to its primality (bool),
        # and send the dict back via future.
        pass


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
