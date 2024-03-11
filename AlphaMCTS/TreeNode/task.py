import numpy as np
import math

from TicTacToe.Board.task import Board


class Node:
    def __init__(self, game, args, board_state, parent=None, action_taken=None, prior=0):
        # game (TicTacToe in our case)
        self.game = game
        # some hyperparameters
        self.args = args
        self.state = board_state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        # make sure that action_taken is None only for root
        if parent is None:
            assert action_taken is None
        if action_taken is None:
            assert parent is None

        self.children = []
        self.expandable_moves = game.get_valid_moves(board_state)

        self.visit_count = 0
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
        return len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return (q_value +
                self.args['C']
                * (math.sqrt(self.visit_count)
                   / (child.visit_count + 1)) * child.prior)

    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = Board()
                child_state.pieces = self.state.pieces.copy()
                child_state = self.game.get_next_state(child_state, 1, action)
                child_state = self.game.change_perspective(child_state, player=-1)

                child = Node(self.game, self.args, board_state=child_state, parent=self,
                             action_taken=action, prior=prob)
                self.children.append(child)

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = self.game.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)
