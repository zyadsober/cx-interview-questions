## Documentation

## Introduction
This is the implementation for the shopping basket challenge. Since the question is stated to be "deliberately open-ended", I have made some assumptions which are listed in this document

## Running the code
The tests can be run using built in python 3 unittest module `python3 -m unittest`

## Method of calculating the best offer combination:
The code uses a recursive DFS approach of exploring the different combinations of offers while keeping track of the best combination found. As a graph, the state which is the remaining items in the basket after applying the previously chosen offer represents vertices while the offers themselves represent the edges. The base case is when no discount can apply to the remaining items.

## Assumptions:
- A basket cannot apply two different offers to the same product:

    For example: Given a product X and offers Y and Z, offer Y gives a percentage discount on product X, offer Z gives a buy 2 get 1 free. If a basket contains a quantity of 3 for item X, then only one of the offers may apply to a single item when calculating the discount.
