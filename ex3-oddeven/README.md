# Odd-Even Sort Tutorial

## Overview
This exercise guides you through implementing a parallel odd-even sort algorithm in Charm4py using channels.

## How Odd-Even Sort Works
Odd-even sort is a parallel sorting algorithm that repeatedly compares and swaps adjacent elements in alternating phases:
- **Odd phase**: Compare and swap elements at indices (1,2), (3,4), (5,6), etc.
- **Even phase**: Compare and swap elements at indices (0,1), (2,3), (4,5), etc.
- Repeat these phases until the array is sorted

This pattern allows parallel comparisons since non-adjacent pairs are independent.

**The Charm4py implementation**: 
- chares are each assigned a single element
- every chare should establish **channels** to its left and right neighbors, for use during the odd and even phases
- chares should iteratively swap elements appropriately such that the chare array contains the sorted list. this process is outlined below:


**Iterative Odd/Even Swap**:
Every iteration is either odd or even. During even phases, even-indexed chares "lead" the exchange, sending their value to the right and waiting on a response. During odd phases, odd-indexed chares "lead" the exchange, sending to the right and waiting on a response.

During every phase, the leading chare performs the following:
- send value right
- wait on a response `r`
- set `self.value = r`

The receiving chare will instead:
- receive a value `v` from the left
- compare `v` with `self.value`
  - If `v <= self.value` then the pairwise ordering is acceptable. Respond with `v`.
  - Otherwise, the pairwise ordering must be corrected. Respond with `self.value` and update `self.value = v`.

## Instructions

1. **Examine the starter code** in `oddeven.py` to understand the structure
   - chares are initialized with a value between 0 and 100
   - a channel to the left ONLY is initialized for each chare
   - validation functionality is provided for testing purposes
2. **Identify the TODOs** which include initializing a channel to the right and implementing the sort iterations
3. **Test your implementation** using the provided testing infrastructure. Usage: `python oddeven.py <n>` where `n` denotes both the number of elements to be sorted and the number of chares. `n` defaults to 4 if no value is provided.
