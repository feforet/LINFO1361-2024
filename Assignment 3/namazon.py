from search import *
import time

#################
# Problem class #
#################

class NAmazonsProblem(Problem):
    """The problem of placing N amazons on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is an empress at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    """
    def __init__(self, N): #j'ai modif (avant pass)
        self.N = N
        self.initial = tuple([-1] * N) #pour que ce soit hashable
        # self.state = tuple(self.initial)

    def actions(self, state): #j'ai modif (avant pass)
        # if state[-1] != -1:
        #     return []
        # else:
        #     return range(self.N)
        for i in range(len(state)):
            if state[i] == -1:
                for j in range(self.N):
                    if not self.is_attacked(state, j, i):
                        yield (j, i)

    def result(self, state, row): #j'ai modif (avant pass)
        col = state.index(-1)
        new_state = list(state[:])
        new_state[col] = row
        return tuple(new_state)

    def goal_test(self, state): #j'ai modif (avant pass)
        if -1 in state:
            return False
        for i in range (self.N):
            for j in range(i+1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                    return False
                # vérifier si les empresses peuvent se déplacer en 3x2 et 4x1
                if (abs(state[i] - state[j]) == 3 and abs(i - j) == 2) or (abs(state[i] - state[j]) == 2 and abs(i - j) == 3) or (abs(state[i] - state[j]) == 4 and abs(i - j) == 1) or (abs(state[i] - state[j]) == 1 and abs(i - j) == 4):
                    return False
        return True
    
    def h(self, node):
        return self.heuristic_1(node)  # comme ca on peut facilement changer d'heuristique


    def heuristic_1(self, node): #avant return 0
        conflicts = 0
        for col, row in enumerate(node.state):
            print("state[i] =",node.state[col])
            print(type(col), type(row))
            if self.is_attacked(node.state, row, col):
                conflicts += 1
        return conflicts

    def is_attacked(self, state, row, col):
            for i in range(len(state)):
                if state[i] != -1:
                    print("state[i] =",state[i])
                    row_of_tuple, *_ = state[i]
                    if row_of_tuple == row or abs(row_of_tuple - row) == abs(i - col):
                        return True
                    elif abs(row_of_tuple - row) == 3 and abs(i - col) == 2:
                        return True
                    elif abs(row_of_tuple - row) == 4 and abs(i - col) == 1:
                        return True
            return False


def successive_boards(node):
    result = ""
    path = node.path()
    for node in path:
        state_str = ""
        for value in node.state:
            if value == -1:
                state_str += len(node.state) * "#"
            else:
                state_str += value * "#"
                state_str += "A"
                state_str += (len(node.state) - value - 1) * "#"
            state_str += "\n"
        result += state_str + "\n\n"
    return result

#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))

start_timer = time.perf_counter()

node = astar_search(problem) #j'ai modif (avant TODO)
# node = breadth_first_graph_search(problem)
#node = depth_first_graph_search(problem)

end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

print(successive_boards(node))

# for node in path: 
#     for value in range(len(node.state)):
#         if node.state[value] == -1:
#             print("#")
#         else:
#             print("A")

# for node in path:
#     state_str = ""
#     for value in node.state:
#         if value == -1:
#             state_str += "#"
#         else:
#             state_str += "A"
#     print(state_str)
    # print(node.state)  # assuming that the _str_ function of state outputs the correct format

    # print()
    
print("Time: ", end_timer - start_timer)