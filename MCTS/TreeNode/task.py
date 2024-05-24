import math
import numpy as np

from TicTacToe.Board.task import Board


class Node:
    def __init__(self, game, args, board_state, parent=None, action_taken=None):
        # game (TicTacToe in our case)
        self.game = game
        # some hyperparameters
        self.args = args
        self.state = board_state
        self.parent = parent
        self.action_taken = action_taken

        # make sure that action_taken is None only for root
        if parent is None:
            assert action_taken is None
        if action_taken is None:
            assert parent is None

        self.children = []
        # add calculation for expandable moves
        self.expandable_moves = board_state.get_valid_moves()

        # The number of times the node has been visited during the simulation phase of MCTS
        self.visit_count = 0
        # The accumulated score associated with that node.
        self.value_sum = 0

    def get_player(self):
        # use state to get the current player. If no action was taken, then player should be None
        if self.action_taken is None:
            return None
        size = self.state.size
        row = self.action_taken // size
        column = self.action_taken % size
        return self.state[row, column]

    def is_fully_expanded(self):
        # check if this node can be expanded
        return np.sum(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        # selection phase
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        # we want to put the opponent in a bad position, so invert the score
        q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * math.sqrt(math.log(self.visit_count) / child.visit_count)

    def expand(self):
        # implement expansion step
        action = np.random.choice(np.where(self.expandable_moves == 1)[0])
        self.expandable_moves[action] = 0

        child_state = self.game.get_board().create_new_board()
        child_state.pieces = self.state.pieces.copy()
        # instead of changing the player, it's easier to change node.game.change_perspective
        child_state = self.game.get_next_state(child_state, 1, action)
        child_state = self.game.change_perspective(child_state, player=-1)

        # new child creation
        child = Node(self.game, self.args, board_state=child_state, parent=self, action_taken=action)
        self.children.append(child)
        return child

    def simulate(self):
        # implement simulation step
        value = self.game.get_game_ended(self.state, self.get_player())
        value = self.game.get_opponent_value(value)

        if value:
            return value

        rollout_state = Board(self.state.size)
        rollout_state.pieces = self.state.pieces.copy()
        rollout_player = 1
        while True:
            valid_moves = rollout_state.get_valid_moves()
            action = np.random.choice(np.where(valid_moves == 1)[0])
            rollout_state = self.game.get_next_state(rollout_state, rollout_player, action)
            value = self.game.get_game_ended(rollout_state, rollout_player)
            if value:
                if rollout_player == -1:
                    value = self.game.get_opponent_value(value)
                return value

            rollout_player = self.game.get_opponent(rollout_player)

    def backpropagate(self, value):
        # implement a backpropagation step. Hint: do not forget to switch value when passing it to the parent
        self.value_sum += value
        self.visit_count += 1

        value = self.game.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)
