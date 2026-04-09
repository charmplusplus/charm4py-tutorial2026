# Exercise 1: Basic examples

These are a collection of Charm4Py examples that show the basic syntax and
structure of Charm4Py programs, and how to run them.

## Hello World (group_hello.py)

This is a Hello World example that prints Hello from all PEs. A message is sent in a ring, starting from PE 0, and the print occurs when the message arrives on a PE.
To run this, use this command:  

`python3 -m charmrun.start +p<N> group_hello.py`

