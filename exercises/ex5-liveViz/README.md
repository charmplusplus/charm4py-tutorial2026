
**Exercise 5: Live visualization of particle exercise (ex4)**

This exercise demonstrates the liveViz capabilities of Charm4Py.
Refer to the liveViz documentation (https://charm4py.readthedocs.io/en/latest/liveviz.html) to learn how to run liveViz
and how to add liveViz calls to your code. Once complete, run the particle code in one terminal
and the liveViz client in another to view the movement of the particles.   

For a simple example of liveViz code (and one that you can run if you run out of time here), there is an example in the Charm4Py repo, in examples/liveviz/liveViz.py.

***Load balancing***

LiveViz helps visually demonstrate how load balancers work in Charm++. You can experiment with this
by adding command-line arguments like `+GreedyLB` for the load balancer using a greedy algorithm and 
`+GreedyRefineLB`, which adds a control to limit the number of migrations.