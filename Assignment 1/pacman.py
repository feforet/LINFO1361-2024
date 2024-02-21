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

    class Action:
        def __init__(self, direction, number_of_moves):
            self.direction = direction
            self.number_of_moves = number_of_moves


    def actions(self, state):
        # Define the possible actions for a given state
        actions = []
        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                if state.grid[i][j] == "P":
                    pos = (i, j)

        x, y = pos
        for k in range(1, state.shape[0]):
            if x+k >= state.shape[0] or state.grid[x+k][y] == "#":
                break
            actions.append(self.Action("S", k))
        for k in range(1, state.shape[0]):
            if x-k < 0 or state.grid[x-k][y] == "#":
                break
            actions.append(self.Action("N", k))
        for k in range(1, state.shape[1]):
            if y+k >= state.shape[1] or state.grid[x][y+k] == "#":
                break
            actions.append(self.Action("E", k))
        for k in range(1, state.shape[1]):
            if y-k < 0 or state.grid[x][y-k] == "#":
                break
            actions.append(self.Action("W", k))

        return actions


    def result(self, state, action):
        # Apply the action to the state and return the new state
        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                if state.grid[i][j] == "P":
                    pos = (i, j)

        x, y = pos
        new_grid = [list(row) for row in state.grid]
        new_answer = state.answer
        new_grid[x][y] = "."

        if action.direction == "S":
            new_pos = (x+action.number_of_moves, y)
        if action.direction == "N":
            new_pos = (x-action.number_of_moves, y)
        if action.direction == "E":
            new_pos = (x, y+action.number_of_moves)
        if action.direction == "W":
            new_pos = (x, y-action.number_of_moves)
        
        if new_grid[new_pos[0]][new_pos[1]] == "F":
            new_answer -= 1
        new_grid[new_pos[0]][new_pos[1]] = "P"
        
        new_state = State(state.shape, tuple([tuple(row) for row in new_grid]), new_answer, "Move " + action.direction + " " + str(action.number_of_moves))
        return new_state
        
    def goal_test(self, state):
    	#check for goal state
        return state.answer == 0



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
