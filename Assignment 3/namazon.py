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
        state[col] = row
        return state

    def goal_test(self, state): #j'ai modif (avant pass)
        if -1 in state:
            return False
        for i in range (self.N):
            for j in range(i+1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                    return False
        return True
    

    def h(self, node): #j'ai modif (avant return 0)

        return node.state.count(-1)   

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

for n in path:

    print(n.state)  # assuming that the _str_ function of state outputs the correct format

    print()
    
print("Time: ", end_timer - start_timer)