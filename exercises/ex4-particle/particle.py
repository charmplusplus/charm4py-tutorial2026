from charm4py import charm, Chare, Array, Reducer, Future, coro, Channel
import time
import random
import math
import array
import sys

# See README.rst

# more info about load balancing command-line options here:
# https://charm.readthedocs.io/en/latest/charm++/manual.html#compiler-and-runtime-options-to-use-load-balancing-module
sys.argv += ['+LBCommOff', '+LBObjOnly']

NUM_ITER = 100
SIM_BOX_SIZE = 100.0


class Particle(object):

    def __init__(self, x, y):
        self.coords = [x, y]  # coordinate of this particle in the 2D space

    def perturb(self, cellsize):
        """ randomly move the particle """
        for i in range(len(self.coords)):
            self.coords[i] += random.uniform(-cellsize[i]*0.1, cellsize[i]*0.1)
            # if particle goes out of bounds of the simulation space, appear on the other side
            if self.coords[i] > SIM_BOX_SIZE:
                self.coords[i] -= SIM_BOX_SIZE
            elif self.coords[i] < 0:
                self.coords[i] += SIM_BOX_SIZE


class Cell(Chare):

    def __init__(self, array_dims, max_particles_per_cell_start, sim_done_future):
        # store future to notify main function when simulation is done
        self.sim_done_future = sim_done_future
        self.iteration = 0
        cellsize = (SIM_BOX_SIZE / array_dims[0], SIM_BOX_SIZE / array_dims[1])
        self.cellsize = cellsize

        # create particles in this cell, in random positions
        self.particles = []
        N = self.getInitialNumParticles(array_dims, max_particles_per_cell_start, cellsize)
        lo_x = self.thisIndex[0] * cellsize[0]  # x coordinate of lower left corner of my cell
        lo_y = self.thisIndex[1] * cellsize[1]  # y coordinate of lower left corner of my cell
        for _ in range(N):
            self.particles.append(Particle(random.uniform(lo_x, lo_x + cellsize[0] - 0.001),
                                           random.uniform(lo_y, lo_y + cellsize[1] - 0.001)))

        # obtain list of my neighbors in the 2D cell grid, and establish a Channel with each
        self.neighbor_indexes = self.getNbIndexes(array_dims)
        self.neighbors = [Channel(self, remote=self.thisProxy[idx]) for idx in self.neighbor_indexes]

    def getInitialNumParticles(self, dims, max_particles, cellsize):
        # return the number of particles to create on this cell at the start of
        # the simulation. The cells that are closer to the grid center start
        # with max_particles particles, the rest start with 0
        grid_center = (SIM_BOX_SIZE / 2, SIM_BOX_SIZE / 2)
        cell_center = (self.thisIndex[0] * cellsize[0] + cellsize[0] / 2,
                       self.thisIndex[1] * cellsize[1] + cellsize[1] / 2)
        dist = math.sqrt((cell_center[0] - grid_center[0])**2 + (cell_center[1] - grid_center[1])**2)
        if dist <= SIM_BOX_SIZE / 5:
            return max_particles
        else:
            return 0

    def getNbIndexes(self, arrayDims):
        # return indexes of neighboring cells (N,NE,E,SE,S,SW,W,NW) with wrap around
        nbs = set()
        x, y = self.thisIndex
        nb_x_coords = [(x-1)%arrayDims[0], x, (x+1)%arrayDims[0]]
        nb_y_coords = [(y-1)%arrayDims[1], y, (y+1)%arrayDims[1]]
        for nb_x in nb_x_coords:
            for nb_y in nb_y_coords:
                if (nb_x, nb_y) != self.thisIndex:
                    nbs.add((nb_x, nb_y))
        return list(nbs)

    def getNumParticles(self):
        return len(self.particles)

    @coro
    def run(self):
        """ this is the simulation loop of each cell """
        cellsize = self.cellsize
        while self.iteration < NUM_ITER:
            # in each iteration, this cell's particles move randomly. some
            # particles might move out of the boundary of this cell, and need
            # to be sent to neighboring cells.
            # We could directly send the list of outgoing particles to each
            # neighbor cell, but this would cause Charm4py to pickle a possibly
            # long list of Particle objects, and is not the most efficient
            # option. Instead, for each neighbor, we insert the particle data
            # of outgoing particles into an array, and send that. This bypasses
            # pickling (Charm4py copies the contents of the array buffer
            # directly into a message)

            """TODO: Implement the simulation loop. This loop needs to do the following in each iteration:
            1. Move each particle randomly by calling the perturb() method of the Particle class.
            2. Check if any particle has moved out of the boundary of this cell. If so, determine which neighboring cell it should be sent to, and add its data to the outgoingParticles array for that neighbor. Remove the particle from this cell's particle list.
            3. Send the outgoingParticles array to each neighboring cell using the corresponding Channel.
            4. Receive incoming particles from neighboring cells using iawait on the list of Channels. For each incoming message, convert the received array of particle data back into Particle objects and add them to this cell's particle list.
            5. Every 10 iterations, perform a reduction to report the current max particles per cell by calling the reportMax method on the (0,0) cell with the current number of particles in this cell, using Reducer.max.
            6. Every 20 iterations, call AtSync to indicate that this cell is ready for load balancing, and then exit the coroutine to allow load balancing to occur. After load balancing, the resumeFromSync method will be called to resume the simulation.
            7. Increment the iteration counter and continue to the next iteration of the loop until NUM_ITER is reached. After the loop, perform a reduction to signal that the simulation is done by reducing on sim_done_future.
            """

            pass

        # simulation done (when all the cells reach this point)
        self.reduce(self.sim_done_future)

    # this is called by the runtime when load balancing finishes. the cell
    # might be on a different PE after load balancing
    def resumeFromSync(self):
        # resume the simulation by calling 'run' again. Note that 'run' is
        # written to be able to continue where it left off
        self.thisProxy[self.thisIndex].run()

    def reportMax(self, max_particles):
        print('Max particles per cell= ' + str(max_particles))


def main(args):
    print('\nUsage: particle.py [num_chares_x num_chares_y] [max_particles_per_cell_start]')
    if len(args) >= 3:
        array_dims = (int(args[1]), int(args[2]))
    else:
        array_dims = (8, 4)  # default: 2D chare array of 8 x 4 cells
    if len(args) == 4:
        max_particles_per_cell_start = int(args[3])
    else:
        max_particles_per_cell_start = 10000

    print('\nCell array size:', array_dims[0], 'x', array_dims[1], 'cells')

    # create 2D Cell chare array and start simulation
    sim_done = Future()
    cells = Array(Cell, array_dims,
                  args=[array_dims, max_particles_per_cell_start, sim_done],
                  useAtSync=True)
    num_particles_per_cell = cells.getNumParticles(ret=True).get()
    print('Total particles created:', sum(num_particles_per_cell))
    print('Initial conditions:\n\tmin particles per cell:', min(num_particles_per_cell),
          '\n\tmax particles per cell:', max(num_particles_per_cell))
    print('\nStarting simulation')
    t0 = time.time()
    cells.run()  # this is a broadcast
    # wait for the simulation to finish
    sim_done.get()
    print('Particle simulation done, elapsed time=', round(time.time() - t0, 3), 'secs')
    exit()


charm.start(main)
