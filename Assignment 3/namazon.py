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
        possible_actions = []
        if state[-1] != -1:
            return possible_actions
        col = state.index(-1)
        for row in range(self.N):
            if not self.is_attacked(state, row, col):
                possible_actions.append(row)
        return possible_actions

    def result(self, state, row): #j'ai modif (avant pass)
        col = state.index(-1)
        new_state = list(state[:])
        new_state[col] = row
        return tuple(new_state)

    def goal_test(self, state): #j'ai modif (avant pass)
        if -1 in state:
            return False
        for col in range (self.N):
            row = state[col]
            if (self.is_attacked(state, row, col)):
                return False
            # for j in range(i+1, self.N):
            #     if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
            #         return False
            #     # vérifier si les empresses peuvent se déplacer en 3x2 et 4x1
            #     if (abs(state[i] - state[j]) == 3 and abs(i - j) == 2) or (abs(state[i] - state[j]) == 2 and abs(i - j) == 3) or (abs(state[i] - state[j]) == 4 and abs(i - j) == 1) or (abs(state[i] - state[j]) == 1 and abs(i - j) == 4):
            #         return False
        return True
    
    def h(self, node):
        return self.heuristic_1(node)  # comme ca on peut facilement changer d'heuristique


    def heuristic_1(self, node): #avant return 0
        conflicts = 0
        for col in node.state:
            row = node.state[col]
            if self.is_attacked(node.state, row, col):
                conflicts += 1
        return conflicts

    def is_attacked(self, state, row, col):
            N = len(state)
            for col_to_check in range(N):
                if state[col_to_check] == -1:
                    break
                if (col_to_check == col):
                    continue
                row_to_check = state[col_to_check]
                if row_to_check == row or abs(row_to_check - row) == abs(col_to_check - col):
                    return True
                if abs(row_to_check - row) == 1 and abs(col_to_check - col) == 4:
                    return True
                if abs(row_to_check - row) == 2 and abs(col_to_check - col) == 3:
                    return True
                if abs(row_to_check - row) == 3 and abs(col_to_check - col) == 2:
                    return True
                if abs(row_to_check - row) == 4 and abs(col_to_check - col) == 1:
                    return True
            return False


def successive_boards(node):
    N = len(node.state)
    result = ""
    path = node.path()
    for node in path:
        state = [["#" for _ in range(N)] for _ in range(N)]
        for col in range(N):
            row = node.state[col]
            if (row != -1):
                state[row][col] = "A"
        state_str = ""
        for row in range(N):
            for col in range(N):
                state_str += state[row][col]
            state_str += "\n"
        result += state_str + "\n"
    result = result.strip()
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