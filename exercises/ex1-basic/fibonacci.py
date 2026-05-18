from charm4py import charm, Chare, Future, coro
#modeled after the charm with futures example in the charm++ textbook

THRESHOLD = 20

class Fib(Chare):

    @coro
    def __init__(self, n, future):
        if n < THRESHOLD:
            res = self.seqFib(n)
            future.send(res)
        else:
            # TODO: Create two futures for the recursive calls

            # TODO: Create two new chares with parameters n - 1, n - 2, and their corresponding futures

            # TODO: Wait for the results and compute res = val1 + val2

            # TODO: Send result back to the parent chare
            pass

    def seqFib(self, n):
        if n <= 1:
            return n
        else:
            return self.seqFib(n - 1) + self.seqFib(n - 2)

@coro
def main(args):
    if len(args) < 2:
        print("Possible Usage: charmrun ++local +p4 fibonacciWithFutures.py <n>")
        charm.exit()
    n = int(args[1])
    if n < 0:
        print("n must be a non-negative integer")
        charm.exit()

    # TODO: Create a future

    # TODO: Create a Fib chare to start the calculations

    # TODO: Get the value of the future (blocks until received) and print it
    charm.exit()

charm.start(main)
