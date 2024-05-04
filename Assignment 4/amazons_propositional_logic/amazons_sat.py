from clause import *

"""
For the n-amazon problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the n-amazons problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Here is an example presenting how to create a clause:
Let's assume that the length/width of the chessboard is 4.
To create a clause X_0_1 OR ~X_1_2 OR X_3_3
you can do:

clause = Clause(4)
clause.add_positive(0, 1)
clause.add_negative(1, 2)
clause.add_positive(3, 3)

The clause must be initialized with the length/width of the chessboard.
The reason is that we use a 2D index for our variables but the format
imposed by MiniSAT requires a 1D index.
The Clause class automatically handle this change of index, but needs to know the
number of column and row in the chessboard.

X_0_0 is the literal representing the top left corner of the chessboard
"""


def get_expression(size: int, placed_amazons: list[(int, int)]) -> list[Clause]:
    """
    Defines the clauses for the N-amazons problem
    :param size: length/width of the chessboard
    :param placed_amazons: a list of the already placed amazons
    :return: a list of clauses
    """

    expression = []
    # your code here
    # 1
    for i in range(size):
        clause = Clause(size)
        for j in range(size):
            clause.add_positive(i, j)
        expression.append(clause)
    # 2
    for i in range(size):
        for a in range(size - 1):
            for b in range(a + 1, size):
                clause = Clause(size)
                clause.add_negative(i, a)
                clause.add_negative(i, b)
                expression.append(clause)
    # 3
    for j in range(size):
        clause = Clause(size)
        for i in range(size):
            clause.add_positive(i, j)
        expression.append(clause)
    # 4
    for j in range(size):
        for a in range(size - 1):
            for b in range(a + 1, size):
                clause = Clause(size)
                clause.add_negative(a, j)
                clause.add_negative(b, j)
                expression.append(clause)
    # 5
    for i, j in placed_amazons:
        clause = Clause(size)
        clause.add_positive(i, j)
        expression.append(clause)
    # 6 and 7
    for i in range(size):
        for j in range(size):
            for a in range(1, size):
                if (i + a < size) and (j + a < size):
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i + a, j + a)
                    expression.append(clause)
                if (i + a < size) and (0 <= j - a):
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i + a, j - a)
                    expression.append(clause)
    # 8
    for i in range(size):
        for j in range(size):
            pairs = [(1,4), (2,3), (3,2), (4,1),
                     (1,-4), (2,-3), (3,-2), (4,-1),
                     (-1,4), (-2,3), (-3,2), (-4,1),
                     (-1,-4), (-2,-3), (-3,-2), (-4,-1)]
            for a, b in pairs:
                if (0 <= i + a < size) and (0 <= j + b < size):
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i + a, j + b)
                    expression.append(clause)

    return expression
