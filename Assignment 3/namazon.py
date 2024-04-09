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
        self.initial = [-1] * N

    def actions(self, state): #j'ai modif (avant pass)
        if state[-1] != -1:
            return []
        else:
            return range(self.N)

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
        return True
    

    def h(self, node): #avant return 0
        # print("I came here \n")
        state = node.state
        # Initialize the heuristic value
        heuristic_value = 0
        
        # Check each column
        for col in range(self.N):
            # If there's already an empress in this column, move to the next column
            if state[col] != -1:
                continue
            
            # Calculate the maximum coverage for placing an empress in this column
            max_coverage = 0
            
            # Check all possible rows in this column
            for row in range(self.N):
                # Check if placing an empress in this position is valid
                valid_placement = True
                
                # Check if there's already an empress on the same row
                if row in state:
                    valid_placement = False
                else:
                    # Check if the empress can attack other empresses diagonally
                    for prev_col, prev_row in enumerate(state[:col]):
                        if prev_row != -1 and abs(row - prev_row) == abs(col - prev_col):
                            valid_placement = False
                            break
                            
                    # Check if the empress can move in 3x2 and 4x1 steps to attack other empresses
                    for prev_col, prev_row in enumerate(state[:col]):
                        if prev_row != -1 and ((abs(row - prev_row) == 3 and abs(col - prev_col) == 2) or
                                            (abs(row - prev_row) == 2 and abs(col - prev_col) == 3) or
                                            (abs(row - prev_row) == 4 and abs(col - prev_col) == 1) or
                                            (abs(row - prev_row) == 1 and abs(col - prev_col) == 4)):
                            valid_placement = False
                            break
                
                # If placing an empress in this position is valid, update the maximum coverage
                if valid_placement:
                    coverage = 1  # Start with one cell (the empress itself)
                    # Count the cells covered by the empress in queen-like movement
                    for i in range(self.N):
                        if i != col:
                            if state[i] == -1 or abs(row - state[i]) == abs(col - i):
                                coverage += 1
                    max_coverage = max(max_coverage, coverage)
                    
            # Add the maximum coverage for this column to the heuristic value
            heuristic_value += max_coverage
        # if(heuristic_value >= 1):
        #     print("heuristic value is : \n", heuristic_value)  
        return -heuristic_value


#####################
# Launch the search #
#####################

problem = NAmazonsProblem(int(sys.argv[1]))

start_timer = time.perf_counter()

node = astar_search(problem) #j'ai modif (avant TODO)

end_timer = time.perf_counter()


# example of print
path = node.path()

print('Number of moves: ', str(node.depth))

# for node in path: 
#     for value in range(len(node.state)):
#         if node.state[value] == -1:
#             print("#")
#         else:
#             print("A")

for node in path:
    state_str = ""
    for value in node.state:
        if value == -1:
            state_str += "#"
        else:
            state_str += "A"
    print(state_str)
    # print(n.state)  # assuming that the _str_ function of state outputs the correct format

    # print()
    
print("Time: ", end_timer - start_timer)