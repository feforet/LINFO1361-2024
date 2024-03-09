from agent import Agent
import random
import math

class Node:
    """Node Class

    A node in the MCTS tree.

    Attributes:
        parent (Node): The parent node of this node.
        state (ShobuState): The game state represented by this node.
        U (int): The total reward of the node. 
        N (int): The number of times the node has been visited.
        children (dict[Node, ShobuAction]): A dictionary mapping child nodes to their corresponding actions that lead to the state they represent.
    """
    def __init__(self, parent, state):
        """Initializes a new Node object.

        Args:
            parent (Node): The parent node of this node.
            state (ShobuState): The game state represented by this node.
        """
        self.parent = parent
        self.state = state
        self.U = 0
        self.N = 0
        self.children = {}

class UCTAgent(Agent):
    """An agent that uses the UCT algorithm to determine the best move.

    This agent extends the base Agent class, providing an implementation of the play
    method that utilizes UCT version of the MCTS algorithm.

    Attributes:
        player (int): The player id this agent represents.
        game (ShobuGame): The game the agent is playing.
        iteration (int): The number of simulations to perform in the UCT algorithm.
    """

    def __init__(self, player, game, iteration):
        """Initializes a UCTAgent with a specified player, game, and number of iterations.

        Args:
            player (int): The player id this agent represents.
            game (ShobuGame): The game the agent is playing.
            iteration (int): The number of simulations to perform in the UCT algorithm.
        """
        super().__init__(player, game)
        self.iteration = iteration

    def play(self, state, remaining_time):
        """Determines the next action to take in the given state.

        Args:
            state (ShobuState): The current state of the game.
            remaining_time (float): The remaining time in seconds that the agent has to make a decision.

        Returns:
            ShobuAction: The chosen action.
        """
        return self.uct(state)

    def uct(self, state):
        """Executes the UCT algorithm to find the best action from the current state.

        Args:
            state (ShobuState): The current state of the game.

        Returns:
            ShobuAction: The action leading to the best-perceived outcome based on UCT algorithm.
        """
        root = Node(None, state)
        root.children = {Node(root, self.game.result(root.state, action)): action for action in self.game.actions(root.state) }
        for _ in range(self.iteration):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child.state)
            self.back_propagate(result, child)
        max_state = max(root.children, key=lambda n: n.N)
        return root.children.get(max_state)

    def select(self, node): # J'imagine que c'est bon vu qu'ils disent rien dessus sur inginious, mais elle timeout...
        """Selects a leaf node using the UCB1 formula to maximize exploration and exploitation.

        A node is considered a leaf if it has a potential child from which no simulation has yet been initiated or when the game is finished.

        Args:
            node (Node): The node to select from.

        Returns:
            Node: The selected leaf node.
        """
        current = node
        while not self.game.is_terminal(current.state):
            if all(child.N > 0 for child in current.children):
                current = max(current.children, key=self.UCB1)
            else:
                break
        return current
    
    def expand(self, node): # C'est bon normalement !
        """Expands a node by adding a child node to the tree for an unexplored action.

        If no child has been initialized for this node, the function initializes a child node for each action and store them in the children dictionary.
        The function then selects one of the unexplored child nodes and returns it. If the node represents a terminal state it effectively returns the node itself, 
        indicating that the node cannot be expanded further.

        Args:
            node (Node): The node to expand. This node represents the current state from which we want to explore possible actions.

        Returns:
            Node: The newly created child node representing the state after an unexplored action. If the node is at a terminal state, the node itself is returned.
        """
        if self.game.is_terminal(node.state):
            return node
        if len(node.children) == 0:
            node.children = {Node(node, self.game.result(node.state, action)): action for action in self.game.actions(node.state)}
        tmp = random.choice([child for child in node.children if child.N == 0])
        tmp.children = {Node(tmp, self.game.result(tmp.state, action)): action for action in self.game.actions(tmp.state)}
        return tmp

    def simulate(self, state): # J'imagine que c'est bon vu qu'ils disent rien dessus sur inginious
        """Simulates a random play-through from the given state to a terminal state.

        Args:
            state (ShobuState): The state to simulate from.

        Returns:
            float: The utility value of the terminal state for the opponent of the player whose turn it is to play in that state.
        """
        round = 0
        while (not self.game.is_terminal(state)) and (round < 500):
            action = random.choice(self.game.actions(state))
            state = self.game.result(state, action)
            round += 1
        return state.utility if state.to_move == 0 else (-state.utility)

    def back_propagate(self, result, node): # Elle est bonne !
        """Propagates the result of a simulation back up the tree, updating node statistics.

        Args:
            result (float): The result of the simulation.
            node (Node): The node to start backpropagation from.
        """
        while node is not None:
            node.N += 1
            if result == 1:
                node.U += 1
            node = node.parent
            result = - result

    def UCB1(self, node): # Your UCB1 implementation doesn't return the right value when N is not 0
        """Calculates the UCB1 value for a given node. Returns infinity if the node has not been visited yet.

        Args:
            node (Node): The node to calculate the UCB1 value for.

        Returns:
            float: The UCB1 value.
        """
        return node.U / node.N + math.sqrt(2 * math.log(node.parent.N) / node.N) if node.N != 0 else float('inf')