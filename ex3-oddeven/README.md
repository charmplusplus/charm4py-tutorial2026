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
- chares should swap elements appropriately such that the chare array contains the sorted list
- every chare should establish **channels** to its left and right neighbors, for use during the odd and even phases

## Objective
Complete the `oddeven.py` file by filling in the missing sections to create a working odd-even sort implementation.

## Instructions

1. **Examine the starter code** in `oddeven.py` to understand the structure
2. **Identify the blanks** marked in the code where you need to add logic
3. **Implement the missing sections:**

4. **Test your implementation** using the provided testing infrastructure. Usage: `python oddeven.py <n>` where `n` denotes both the number of elements to be sorted and the number of chares.
