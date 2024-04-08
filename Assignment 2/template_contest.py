from agent import Agent
import random
import numpy as np
import time
from decimal import *
from typing import NamedTuple, List, Set

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
        self.max_depth = 6
        self.tree = {}
        self.transposition_table = {}
        self.start_time = time.time()
        self.actions_to_evaluate = List[None]

    def play(self, state, remaining_time):
        """Determines the next action to take in the given state.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The chosen action.
        """
        
        return self.iterative_deepening(state)

    def is_cutoff(self, state, depth):
        """Determines if the search should be cut off at the current depth.

        Args:
            state (ShobuState): The current state of the game.
            depth (int): The current depth in the search tree.

        Returns:
            bool: True if the search should be cut off, False otherwise.
        """
        return depth >= self.max_depth or self.game.utility(state,self.player) != 0
    
    def eval(self, state, depth):
        """Evaluates the given state and returns a score from the perspective of the agent's player.

        Args:
            state (ShobuState): The game state to evaluate.

        Returns:
            float: The evaluated score of the state.
        """
        if self.game.utility(state, self.player) != 0:
            return 10 * self.game.utility(state, self.player)

        n_pieces_me = 0
        n_pieces_opponent = 0
        min_me = 4 # 4 boards
        min_opponent = 4
        me = self.player # 1 or 0
        opponent = 1 - self.player
        # my_mobility = len(state.actions)
        # opponent_mobility = len(self.game.result(state, None).actions)
        for i in range(4):
            if (len(state.board[i][opponent]) == 0):
                return 10
            n_pieces_me += len(state.board[i][me])
            n_pieces_opponent += len(state.board[i][opponent])
            min_me = min(min_me, len(state.board[i][me]))
            min_opponent = min(min_opponent, len(state.board[i][opponent]))
        
        res = 0.4*(n_pieces_me - n_pieces_opponent)/16 + 0.6*(min_me - min_opponent)/4
        return res
    
    def check_time (self, start_time, time_limit):
        if time.time() - start_time <= 300 - time_limit: 
            return True
        return False

    def alpha_beta_search(self, state, remaining_time):
        """Implements the alpha-beta pruning algorithm to find the best action.

        Args:
            state (ShobuState): The current game state.

        Returns:
            ShobuAction: The best action as determined by the alpha-beta algorithm.
        """
        _, action = self.max_value(state, -float("inf"), float("inf"), 0)
        return action


    def max_value(self, state, alpha, beta, depth,start_time):
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

        if self.check_time(self.start_time, 200) or state.count_boring_actions >= 10:
            self.max_depth = 7
        elif self.check_time(self.start_time, 125):
            self.max_depth = 6
        elif self.check_time(self.start_time, 25):
            self.max_depth = 5


        state_key = str(state.board) + str(state.to_move)
        if state_key in self.transposition_table.keys():
            return self.transposition_table[state_key]

        best_val = -float("inf")
        move = None
        
        for a in self.actions_to_evaluate :
            (val_to_compare, _) = self.min_value(self.game.result(state,a), alpha,beta, depth+1,start_time)
            if (val_to_compare > best_val):
                best_val = val_to_compare
                move = a
            if best_val >= beta :
                return best_val,move
            alpha = max(alpha,best_val)

        self.transposition_table[state_key] = (best_val,move)

        return best_val, move

    def min_value(self, state, alpha, beta, depth,start_time):
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
        
        if self.check_time(self.start_time, 200) or state.count_boring_actions >= 10:
            self.max_depth = 7
        elif self.check_time(self.start_time, 125):
            self.max_depth = 6
        elif self.check_time(self.start_time, 25):
            self.max_depth = 5
        
        state_key = str(state.board) + str(state.to_move)
        if state_key in self.transposition_table.keys():
            # print("I came here in min value \n")
            return self.transposition_table[state_key]
        best_val = float("inf")
        move = None
        # actions = self.game.actions(state)
        # act = sorted(actions,key=lambda a: self.eval(self.game.result(state,a),depth), reverse=False)
        # act = act[0:30]
        
        for a in self.actions_to_evaluate: 
            val_to_compare,_ = self.max_value(self.game.result(state,a), alpha,beta, depth+1,start_time)
            if (val_to_compare < best_val):
                best_val = val_to_compare
                move = a
            if best_val <= alpha :
                return best_val,move
            beta = min(beta,best_val)
        self.transposition_table[state_key] = (best_val,move)
        # print(len(self.transposition_table))
        # print("depth here is : ", depth)

        return best_val, move
    
    def iterative_deepening(self, state):

        act = sorted(self.game.actions(state),key=lambda a: self.eval(self.game.result(state,a),self.max_depth), reverse=True)
        act = act[0:20]

        self.actions_to_evaluate = act

        #self.transposition_table = {}
        val, action = self.max_value(state, -float("inf"), float("inf"), 0,self.start_time)
        return action