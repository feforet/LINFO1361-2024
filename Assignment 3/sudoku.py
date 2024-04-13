import random
import time
import math
import sys


def objective_score(board):
    count_zero = 0
    conflicts = {}
    for i in range(9):
        for j in range(9):
            if (board[i][j] == 0):  # NotFilled
                count_zero += 1
            else:
                for k in range(9):
                    if (board[i][j] == board[k][j]) and (i != k):  # SameColumn
                        conflicts[(i,j,k,j)] = True
                    if (board[i][j] == board[i][k]) and (j != k):  # SameRow
                        conflicts[(i,j,i,k)] = True
                xTopLeft = i - (i % 3)
                yTopLeft = j - (j % 3)
                for k in range(xTopLeft, xTopLeft+3):
                    for l in range(yTopLeft, yTopLeft+3):
                        if (board[i][j] == board[k][l]) and (i!=k or j!=l):  # SameSubGrid
                            conflicts[(i,j,k,l)] = True

    return count_zero + (len(conflicts) / 2)


def simulated_annealing_solver(initial_board):

    """Simulated annealing Sudoku solver."""
    def is_initial(tup):
        i, j = tup
        return initial_board[i][j] != 0

    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution
    
    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 1.0 - 1e-5  #TODO: Adjust this parameter to control the cooling rate

    while temperature > 0.0001:

        try:  

            # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
            neighbor = [row[:] for row in current_solution]
            zero = (random.random() >= 0.5)
            other = True
            i = 0
            # Une chance sur 2 qu'on complète une case vide, une chance sur 2 qu'on modifie une case
            while (not zero) and (i < 9):
                for j in range(9):
                    if (neighbor[i][j] == 0):
                        neighbor[i][j] = random.randint(1, 9)
                        zero = True
                        other = False
                        break
                i += 1
            if (other):
                to_modify = (random.randint(0, 8), random.randint(0, 8))
                while (is_initial(to_modify)):
                    to_modify = (random.randint(0, 8), random.randint(0, 8))
                i, j = to_modify
                neighbor[i][j] = random.randint(1,9)
            # END TODO

            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

            if current_score == 0:

                return current_solution, current_score

            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (neighbor_score > 0 and math.exp((delta/temperature)) > random.random()):

                current_solution = neighbor
                current_score = neighbor_score

                if (current_score < best_score):
                    best_solution = current_solution
                    best_score = current_score

            # Cool down the temperature
            temperature *= cooling_rate
        except:
            print("Break asked")
            break
        
    return best_solution, best_score


def print_board(board):

    """Print the Sudoku board."""

    for row in board:
        print("".join(map(str, row)))
 

def read_sudoku_from_file(file_path):
    """Read Sudoku puzzle from a text file."""
    
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]

    return sudoku
 

if __name__ == "__main__":

    # Reading Sudoku from file
    initial_board = read_sudoku_from_file(sys.argv[1])

    # Solving Sudoku using simulated annealing
    start_timer = time.perf_counter()

    solved_board, current_score = simulated_annealing_solver(initial_board)

    end_timer = time.perf_counter()

    print_board(solved_board)
    print("\nValue(C):", current_score)

    # print("\nTime taken:", end_timer - start_timer, "seconds")