# 2D K-Means Clustering (Chare Arrays)

## Overview
This exercise implements **k-means clustering** of M points in 2D space, distributed across N chares, using the classic Lloyd iterative refinement scheme. Each iteration is one broadcast + two reductions over a chare array.

The algorithm:
1. **Main** generates K random points in `[0, 1)^2` as initial centroid guesses.
2. **Main** broadcasts the K centroids to every `Points` chare's `Assign` entry method.
3. Each chare assigns each of its local points to the nearest centroid (by squared Euclidean distance), and contributes to **two sum reductions**:
   - `counts` -- length-K integer array, number of local points assigned to each cluster,
   - `coords` -- length-2K double array, sum of x and y coordinates of local points assigned to each cluster (interleaved: `x_0, y_0, x_1, y_1, ...`).
4. **Main** receives both reduced arrays. New centroid for cluster `i` is `(coords[2i] / counts[i], coords[2i+1] / counts[i])`. Empty clusters keep their old centroid.
5. **Convergence**: when no centroid coordinate moves by more than `THRESHOLD` (0.001) between successive iterations, stop. Otherwise broadcast the new centroids and repeat.

## Charm4py Concepts Used
- **Chare arrays** (`Array(Points, N, ...)`) -- N chares, each holding a shard of the data.
- **Broadcasts** on a chare array (`points.Assign(...)`) -- one call invokes the entry method on every element.
- **Two concurrent reductions** with `Reducer.sum` -- per-chare lists are element-wise summed and delivered to two distinct futures in the same iteration.
- **Futures** as reduction targets -- main blocks on `f.get()` to receive each reduced array.

## Structure of the Starter Code
- `Points` chare:
  - constructor builds `POINTS_PER_CHARE` random `(x, y)` points (seeded per index so every chare gets a different shard).
  - `assign(centroids, counts_future, coords_future)` -- needs to bin every local point to its closest centroid and contribute to the two sum reductions.
- `main`:
  - sets up the `Points` array and the initial centroid guess (also random in `[0, 1)^2`).
  - drives the iterative loop: broadcast, collect, recompute centroids, check convergence.

## TODOs
The driving algorithm (centroid recomputation, convergence check, final reporting) is all provided. You only need to fill in the per-chare assignment and the two Charm4py communication primitives:

1. **Closest-centroid assignment** -- inside `Points.assign`, for each local point `(x, y)`, find the index of the closest centroid by squared Euclidean distance, then increment `counts[best]` and add the coordinates into `coords[2*best]` and `coords[2*best + 1]`.
2. **Two reductions** -- still inside `Points.assign`, contribute to two sum reductions, one for `counts` (length K) targeting `counts_future`, and one for `coords` (length 2K) targeting `coords_future`. Use `self.reduce(<target>, <value>, Reducer.sum)`.
3. **Broadcast + collect** -- inside `main`'s loop, create two `Future` objects, broadcast `centroids` by calling `assign` on the chare array, and block on each future with `.get()` to receive the reduced `counts` and `coords` arrays.

## Running
```
python -m charmrun.start +p<N> kmeans.py <num_chares> <K>
```
`+pN` runs on N PEs. `num_chares` defaults to 4, `K` defaults to 4. Each chare holds `POINTS_PER_CHARE = 1000` random 2D points uniformly distributed in `[0, 1)^2`.

