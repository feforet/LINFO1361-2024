#!/bin/python3
"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
import sys
from search import *
import signal


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
        x, y = state.pos

        # Looks in each direction for each possible number of tiles (up to the edge of the grid or a wall)
        for k in range(1, state.shape[1]):
            if y-k < 0 or state.grid[x][y-k] == "#":
                break
            actions.append(self.Action("W", k))

        for k in range(1, state.shape[0]):
            if x+k >= state.shape[0] or state.grid[x+k][y] == "#":
                break
            actions.append(self.Action("S", k))

        for k in range(1, state.shape[1]):
            if y+k >= state.shape[1] or state.grid[x][y+k] == "#":
                break
            actions.append(self.Action("E", k))

        for k in range(1, state.shape[0]):
            if x-k < 0 or state.grid[x-k][y] == "#":
                break
            actions.append(self.Action("N", k))

        return tuple(actions)


    def result(self, state, action):
        # Apply the action to the state and return the new state
        x, y = state.pos
        new_grid = [list(row) for row in state.grid]
        new_answer = state.answer
        new_grid[x][y] = "."

        # calculate the new position
        if action.direction == "S":
            new_pos = (x+action.number_of_moves, y)
        if action.direction == "N":
            new_pos = (x-action.number_of_moves, y)
        if action.direction == "E":
            new_pos = (x, y+action.number_of_moves)
        if action.direction == "W":
            new_pos = (x, y-action.number_of_moves)
        
        # check if a fruit is eaten and update the position of the pacman
        if new_grid[new_pos[0]][new_pos[1]] == "F":
            new_answer -= 1
        new_grid[new_pos[0]][new_pos[1]] = "P"

        new_move = f"Move to ({new_pos[0]}, {new_pos[1]})"
        if new_answer == 0:
            new_move += " Goal State"
        
        return State(state.shape, tuple([tuple(row) for row in new_grid]), new_answer, new_move, new_pos)
        
    def goal_test(self, state):
    	# check if there is no more fruit
        return state.answer == 0



###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init", pos=None):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move
        self.pos=pos
        # if the position of the pacman is not given, we look for it
        if self.pos is None:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if self.grid[i][j] == "P":
                        self.pos = (i, j)
                        break
                if self.pos is not None:
                    break

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s

    # we need to define the __eq__ and __hash__ functions to use the state as a key in a dictionary
    def __eq__(self, other):
        return self.grid == other.grid
    def __hash__(self):
        return hash(str(self.grid))


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines() # toutes les lignes du file (row de la grid)
    shape_x, shape_y = tuple(map(int, lines[0].split())) # on regarde la première ligne pour trouver les dims de la grid
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]] #on itère sur la grip (on commence à la ligne 1 et pas 0 puisque ligne 0 = dims jusqu'au bout de la grid) : on a une liste de tuples qui représentent une ligne de la grid
    initial_fruit_count = sum(row.count('F') for row in initial_grid) #compte le nombre de fruit dans la grid

    return (shape_x, shape_y), initial_grid, initial_fruit_count #les dims, toutes les lignes de la grid, le nombre de fruits


def timeout_handler(signum, frame):
    raise TimeoutError("Timeout")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
    filepath = sys.argv[1]

    # Only usefull to compare performance of the search algorithms
    if filepath == "test":
        print("Instance | Search | Time\t| Explored  | Remaining")
        for i in range(1, 11):
            print("-"*55)
            path = f"Instances/i{i:02}"
            shape, initial_grid, initial_fruit_count = read_instance_file(path)
            init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")
            problem = Pacman(init_state)

            for search_func, search_name in [(breadth_first_tree_search, 'bt'), (breadth_first_graph_search, "bg"), (depth_first_tree_search, "dt"), (depth_first_graph_search, "dg")]:
                # prevent infinite loops in tree searches
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(60)
                end_timer = 0.0
                start_timer = time.perf_counter()

                try:
                    node, explored_nodes, remaining_nodes_queue = search_func(problem)
                    end_timer = time.perf_counter()
                    finished = True
                except TimeoutError as e:
                    finished = False
                finally:
                    signal.alarm(0)
                
                if finished:
                    timer = end_timer - start_timer
                    print(f"{path[10: ]}\t | {search_name}\t  | {timer:.5f}\t| {explored_nodes}\t    | {remaining_nodes_queue}")
                else:
                    print(f"{path[10: ]}\t | {search_name}\t  | TIMEOUT")


    else:
        shape, initial_grid, initial_fruit_count = read_instance_file(filepath) #On initialise les variables grâce à la lecture du file
        init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init") #on met en tuple pour que ce soit immuable, on crée le initial state
        problem = Pacman(init_state) #On définit le problème par la classe Pacman

        # Example of search
        start_timer = time.perf_counter()
        node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
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
