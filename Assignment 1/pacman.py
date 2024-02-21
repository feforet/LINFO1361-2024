#!/bin/python3
"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
import sys
from search import *


#################
# Problem class #
#################
dico = {}
class Pacman(Problem):



    def actions(self, state):
        # Define the possible actions for a given state
        pass


    def result(self, state, action):
        # Apply the action to the state and return the new state
        pass
        
    def goal_test(self, state):
    	#check for goal state
    	pass



###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines() # toutes les lignes du file (row de la grid)
    shape_x, shape_y = tuple(map(int, lines[0].split())) # on regarde la première ligne pour trouver les dims de la grid
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]] #on itère sur la grip (on commence à la ligne 1 et pas 0 puisque ligne 0 = dims jusqu'au bout de la grid) : on a une liste de tuples qui représentent une ligne de la grid
    initial_fruit_count = sum(row.count('F') for row in initial_grid) #compte le nombre de fruit dans la grid

    return (shape_x, shape_y), initial_grid, initial_fruit_count #les dims, toutes les lignes de la grid, le nombre de fruits


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
    filepath = sys.argv[1]

    shape, initial_grid, initial_fruit_count = read_instance_file(filepath) #On initialise les variables grâce à la lecture du file
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init") #on met en tuple pour que ce soit immuable, on crée le initial state
    problem = Pacman(init_state) #On définit le problème par la classe Pacman

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
