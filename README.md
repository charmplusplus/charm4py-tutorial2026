# charm4py-tutorial2026
*Materials for the 2026 Charm4Py Tutorial at IPDPS, including examples and slides.*

Many programming models have been developed to implement scalable parallel programs. Charm++ is built around the concept of distributed migratable objects, called chares. This empowers an introspective and adaptive runtime system (aRTS) to support automatic overlap of communication and computation, dynamic load balancing, energy optimization, fault tolerance, and resource elasticity. These signature adaptive capabilities distinguish Charm++ from MPI, the predominant parallel programming model.

Charm4Py is an implementation of the Charm++ programming model that makes these adaptive capabilities available to parallel Python programmers. Charm4Py programs use Python classes to implement chare objects; Charm++ features such as dynamic load balancing and asynchronous communication are made available to Charm4Py programs by linking it with the Charm++ aRTS under the hood. Charm4Py can thus be thought of as Distributed Adaptive Python, a parallel programming model with distributed adaptivity features that is compatible with existing Python conventions, and allows the use of existing popular Python libraries.

This tutorial aims to teach effective parallel programming using Charm4Py. Attendees will start with basic knowledge of Python, and by the end of the tutorial are expected to be able to code sophisticated parallel applications that can run on clusters, supercomputers, and cloud-based resources scalably and adaptively.

### Presenters
Laxmikant Kale, Ritvik Rao, Maya Taylor, and Aditya Bhosale (University of Illinois Urbana-Champaign)

### Tutorial Offerings
- Session 1: Monday, May 25 @ 8:30am-12:00pm
- Session 2: Tuesday, May 26 @ 8:30am-12:00pm

Updated conference schedule [here](https://ssl.linklings.net/conferences/ipdps/ipdps2026_program/views/at_a_glance.html).

### Tutorial Schedule

| Module | Description | Exercises
| -------- | -------- | ----- |
| Introduction | Overview of the Charm4Py programming model with basic examples. Attendees will install the Charm4Py Docker container. | [Ex1](https://github.com/charmplusplus/charm4py-tutorial2026/tree/main/exercises/ex1-basic) | 
| Chare Arrays | Learn about Chare arrays and associated communication primatives, including `broadcasts`, `reductions`, and `channels.`| [Ex2](https://github.com/charmplusplus/charm4py-tutorial2026/tree/main/exercises/ex2-chare-arrays), [Ex3](https://github.com/charmplusplus/charm4py-tutorial2026/tree/main/exercises/ex3-oddeven)| 
| Advanced Features | Discussion of load balancing and GPU integration in Charm4Py. | |
| Profiling and Visualization | Learn how to profile Charm4Py programs with `projections` and how to use the `liveViz` visualization tool. | [Ex4](https://github.com/charmplusplus/charm4py-tutorial2026/tree/main/exercises/ex4-particle), [Ex5]()|

