from agent import Agent
import random
import numpy as np
import time
from decimal import *

class AI(Agent):
    """An agent that plays following your algorithm.

    This agent extends the base Agent class, providing an implementation your agent.

    Attributes:
        player (int): The player id this agent represents.
        game (ShobuGame): The game the agent is playing.
    """

    class Node:
        def __init__(self, state, action, value, children, min_max):
            self.state = state
            self.action = action
            self.value = value
            self.min_max = min_max
            self.children = np.array(children)
            np.sort(self.children)
            if min_max == "max":
                self.children = np.flip(self.children)
        
        def __lt__(self, other):
            return self.value < other.value
        def __gt__(self, other):
            return self.value > other.value
        def __eq__(self, other):
            return self.value == other.value

    def __init__(self, player, game):
        """Initializes an AI instance with a specified player and game.

        Args:
            player (int): The player ID this agent represents (0 or 1).
            game (ShobuGame): The Shobu game instance the agent will play on.
        """
        super().__init__(player, game)
        self.max_depth = 3
        self.tree = {}
        self.transposition_table = {}

    def play(self, state, remaining_time):
        """Determines the next action to take in the given state.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The chosen action.
        """
        
        # Adjust search depth based on remaining time
        # if remaining_time > 300 :  # Example threshold, adjust as needed
        #     self.max_depth = 4 # Longer search for more time
        #     #   print("I have change depth to 4 \n")
        # else :
        #     self.max_depth = 3
        #     # print("I have change depth to 3 \n")
        # # print("remaining_time", remaining_time)
        return self.iterative_deepening(state, remaining_time)

    def is_cutoff(self, state, depth):
        """Determines if the search should be cut off at the current depth.

        Args:
            state (ShobuState): The current state of the game.
            depth (int): The current depth in the search tree.

        Returns:
            bool: True if the search should be cut off, False otherwise.
        """
        return depth >= self.max_depth or state.utility != 0
    
    def eval(self, state, depth):
        """Evaluates the given state and returns a score from the perspective of the agent's player.

        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """
        # min_me = 4 # 4 pieces
        # min_opponent = 4
        # me = self.player # 1 or 0
        # opponent = 1 - self.player
        # # my_mobility = len(self.game.actions(state))
        # # opponent_mobility = len(self.game.actions(state))
        # for i in range(4):
        #     min_me = min(min_me, len(state.board[i][me]))
        #     min_opponent = min(min_opponent, len(state.board[i][opponent]))

        # getcontext().prec = 3
        # print("val returned by eval : \n",Decimal(float(min_me - min_opponent)))
            
        # return float(min_me - min_opponent) 
        #+ my_mobility-opponent_mobility
        # Ton essai
        if state.utility != 0:
            return 1000 * state.utility # * self.max_depth / depth # to make the agent prefer winning faster
        n_moves = len(self.game.actions(state))
        n_pieces_me = 0
        n_pieces_opponent = 0
        min_me = 4 # 4 boards
        min_opponent = 4
        me = self.player # 1 or 0
        opponent = 1 - self.player
        for i in range(4):
            n_pieces_me += len(state.board[i][me])
            n_pieces_opponent += len(state.board[i][opponent])
            min_me = min(min_me, len(state.board[i][me]))
            min_opponent = min(min_opponent, len(state.board[i][opponent]))
            if(len(state.board[i][opponent]) == 0 or len(state.board[i][opponent]) == 1):
                return 1

        # il faut trouver un moyen que la valeur de retour soit bornée entre -1 et 1
        # au chap 23, ils parlent de comment faire du machine learning pour trouver les bons poids
        # print("n_pieces_me \n", n_pieces_me)
        # print("n_pieces_opponent \n", n_pieces_opponent)
        # print("min_me \n", min_me)
        # print("min_opponent \n", min_opponent)
        # if (n_pieces_me - n_pieces_opponent) + 10* (min_me - min_opponent) == 0:
        #     return 0
        # if(n_pieces_me -n_pieces_opponent) < 0:
        #     # print("I came here in eval : my opponent has more pieces than me \n")
        #     return -1
        # if(min_opponent == 0 ):
        #     # print("I came here in eval :This is a win! \n")
        #     return 1
        # if (n_pieces_me - n_pieces_opponent) + 10* (min_me - min_opponent) != 0.3125 and (n_pieces_me - n_pieces_opponent) + 10* (min_me - min_opponent) != -0.3125:
        #     print("Ca vaut : \n",(n_pieces_me - n_pieces_opponent)/16 + (min_me - min_opponent)/4)
        # getcontext().prec = 3
        # print("val returned by eval : \n",Decimal(0.8*(n_pieces_me - n_pieces_opponent)/16 + 0.2*(min_me - min_opponent)/4))
        
        return 0.5*(n_pieces_me - n_pieces_opponent)/16 + 0.5*(min_me - min_opponent)/4

    def alpha_beta_search(self, state, remaining_time):
        """Implements the alpha-beta pruning algorithm to find the best action.

        Args:
            state (ShobuState): The current game state.

        Returns:
            ShobuAction: The best action as determined by the alpha-beta algorithm.
        """
        _, action = self.max_value(state, -float("inf"), float("inf"), 0)
        return action
    
        # start_time = time.time()
        # move = None

        # # Perform iterative deepening until time runs out
        # depth = 2
        # while time.time() - start_time < remaining_time:
        #     val, action = self.max_value(state, -float("inf"), float("inf"), depth)
        #     if time.time() - start_time >= remaining_time:
        #         break  # Exit loop if time runs out
        #     move = action  # Update best action found so far
        #     if val > 0.6 :
        #         return move  # Exit loop if a winning move is found
        #     depth += 1  # Increase depth for the next iteration

        # return move
        # for depth in range(1, self.max_depth + 1):
        #     best_val, move = self.max_value(state, -float("inf"), float("inf"), depth)
        #     print("best_val is : \n",best_val)
        #     if best_val == float("inf"):  # If a winning move is found, return it immediately
        #         return move
        # return move  # Return the best move found in the last iteration


    def max_value(self, state, alpha, beta, depth):
        """Computes the maximum achievable value for the current player at a given state using the alpha-beta pruning.

        This method recursively explores all possible actions from the current state to find the one that maximizes
        the player's score, pruning branches that cannot possibly affect the final decision.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """
        if self.is_cutoff(state,depth) :
            return self.eval(state, depth), None

        state_key = str(state)
        if state_key in self.transposition_table.keys():
            # print("I came here in max value \n")
            return self.transposition_table[state_key]

        best_val = -float("inf")
        move = None
        actions = self.game.actions(state)
        actions.sort(key=lambda a: self.eval(self.game.result(state,a),depth), reverse=True)

        for i in range (1,len(actions)):
            print(self.eval(self.game.result(state,i),depth))
            if (self.eval(self.game.result(state,i-1),depth) < self.eval(self.game.result(state,i),depth)):
                print("it is not correctly sorted in max\n")
        for a in actions :
            (val_to_compare, _) = self.min_value(self.game.result(state,a), alpha,beta, depth+1)
            if (val_to_compare > best_val):
                best_val = val_to_compare
                move = a
            if best_val >= beta :
                return best_val,move
            alpha = max(alpha,best_val)

        self.transposition_table[state_key] = (best_val, move)
        # getcontext().prec = 3
        # print("best_val is :  \n",Decimal(best_val))

        # print(len(self.transposition_table))

        return best_val, move

    def min_value(self, state, alpha, beta, depth):
        """Computes the minimum achievable value for the opposing player at a given state using the alpha-beta pruning.

        Similar to max_value, this method recursively explores all possible actions from the current state to find
        the one that minimizes the opponent's score, again using alpha-beta pruning to cut off branches that won't
        affect the outcome.

        Args:
            state (ShobuState): The current state of the game.
            alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
            beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
            depth (int): The current depth in the search tree.

        Returns:
            tuple: A tuple containing the best value achievable from this state for the opponent and the action that leads to this value.
                If the state is a terminal state or the depth limit is reached, the action will be None.
        """

        if self.is_cutoff(state,depth) :
            return self.eval(state, depth), None
        
        state_key = str(state)
        if state_key in self.transposition_table.keys():
            # print("I came here in min value \n")
            return self.transposition_table[state_key]
        best_val = float("inf")
        move = None
        actions = self.game.actions(state)
        actions.sort(key=lambda a: self.eval(self.game.result(state,a),depth), reverse=True)
        for i in range (1,len(actions)):
            if (self.eval(self.game.result(state,i-1),depth) >  self.eval(self.game.result(state,i),depth)) :
                print("it is not correctly sorted in min \n")
        for a in actions: 
            val_to_compare,_ = self.max_value(self.game.result(state,a), alpha,beta, depth+1)
            # print("val_to_compare is : \n",val_to_compare)
            if (val_to_compare < best_val):
                best_val = val_to_compare
                move = a
            if best_val <= alpha :
                return best_val,move
            beta = min(beta,best_val)
        self.transposition_table[state_key] = (best_val, move)
        # print(len(self.transposition_table))
        # print("depth here is : ", depth)

        return best_val, move
    
    def iterative_deepening(self, state, remaining_time):
        start_time = time.time()

        # Perform iterative deepening until time runs out
        if time.time() - start_time >= remaining_time:
            self.max_depth = 4
        # for depth in range(0, 1000000000000000000000):
        #     print("depth is : ", depth)
        #     if remaining_time > 3
        #     _, action = self.max_value(state, -float("inf"), float("inf"), depth)
        #     if time.time() - start_time >= remaining_time-1:
        #         break
        #     if(self.is_cutoff(state, depth)==False):
        #         return action
        # print("i came here \n")
        # return action