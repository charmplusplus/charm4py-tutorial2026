# Exercise 1: Basic examples

These are a collection of Charm4Py examples that show the basic syntax and
structure of Charm4Py programs, and how to run them.

## Hello World (group_hello.py)

This is a Hello World example that prints Hello from all PEs. A message is sent in a ring, starting from PE 0, and the print occurs when the message arrives on a PE.
To run this, use this command:  

`python3 -m charmrun.start +p<N> group_hello.py`

## Primes exercise

This exercise calculates the primality of multiple large numbers. We have provided the logic of creating chares and recovering results from each chare, and all you have to do is finish the checkPrimality logic to calculate the primality of each number on each chare.   
To run this, use this command:

`python3 -m charmrun.start +p<N> primes.py <K> <num_chares>`

K is the number of integers to check. You can add `--print` as an option to view the results (to check correctness). We have set the maximum size of each generated integer to 10^13 to guarantee a reasonable runtime with a simple primality test. You can decrease the number when checking for accuracy, and increase it if you want to test performance.

## Fibonacci exercise

This exercise calculates Fibonacci numbers in a sequence. You won't be implementing the most efficient method, but this exercise will help you learn how to use futures in Charm4Py. You will complete the portions of the program that create and use the futures.    
To run this program use:

`python3 -m charmrun.start +p<N> fibonacci.py <n>`

n is how many numbers in the Fibonacci sequence to calculate.
