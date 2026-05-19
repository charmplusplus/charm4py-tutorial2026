from charm4py import charm, Chare, Array, Reducer, Future, coro
import random

POINTS_PER_CHARE = 1000
THRESHOLD = 0.001


class Points(Chare):

    def __init__(self, K):
        self.K = K
        # each chare seeds its own RNG so every chare gets a different shard
        rng = random.Random(self.thisIndex[0])
        self.points = [(rng.random(), rng.random())
                       for _ in range(POINTS_PER_CHARE)]

    def assign(self, centroids, counts_future, coords_future):
        # centroids: length-K list of (x, y) tuples
        K = self.K
        counts = [0] * K
        coords = [0.0] * (2 * K)  # interleaved: x0, y0, x1, y1, ..., x_{K-1}, y_{K-1}
        for (x, y) in self.points:
            best = 0
            best_d = (x - centroids[0][0]) ** 2 + (y - centroids[0][1]) ** 2
            for i in range(1, K):
                d = (x - centroids[i][0]) ** 2 + (y - centroids[i][1]) ** 2
                if d < best_d:
                    best_d = d
                    best = i
            counts[best] += 1
            coords[2 * best] += x
            coords[2 * best + 1] += y
        self.reduce(counts_future, counts, Reducer.sum)
        self.reduce(coords_future, coords, Reducer.sum)


@coro
def main(args):
    num_chares = 4
    K = 4
    if len(args) > 1:
        num_chares = int(args[1])
    if len(args) > 2:
        K = int(args[2])

    M = num_chares * POINTS_PER_CHARE
    print(f"K-Means: {M} points across {num_chares} chares, {K} clusters")
    print(f"Convergence threshold: {THRESHOLD}")

    points = Array(Points, num_chares, args=[K])

    # initial centroid guess: K random points in [0, 1)^2
    rng = random.Random(42)
    centroids = [(rng.random(), rng.random()) for _ in range(K)]

    iteration = 0
    while True:
        iteration += 1
        f_counts = Future()
        f_coords = Future()
        points.assign(centroids, f_counts, f_coords)
        counts = f_counts.get()
        coords = f_coords.get()

        # compute new centroids; for empty clusters, keep the old centroid
        new_centroids = []
        for i in range(K):
            if counts[i] == 0:
                new_centroids.append(centroids[i])
            else:
                new_centroids.append((coords[2 * i] / counts[i],
                                      coords[2 * i + 1] / counts[i]))

        # convergence: no centroid coordinate moves by more than THRESHOLD
        max_change = max(
            max(abs(new_centroids[i][0] - centroids[i][0]),
                abs(new_centroids[i][1] - centroids[i][1]))
            for i in range(K)
        )
        centroids = new_centroids
        if max_change < THRESHOLD:
            break

    print(f"Converged in {iteration} iterations")
    print("Final centroids:")
    for i, c in enumerate(centroids):
        print(f"  cluster {i}: ({c[0]:.4f}, {c[1]:.4f})  count = {counts[i]}")
    exit()


charm.start(main)
