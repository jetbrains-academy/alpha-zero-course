import numpy as np
import math

from TicTacToe.Board.task import Board


class Node:
    def __init__(self, game, args, board_state, parent=None, action_taken=None, prior=0):
        self.game = game
        self.args = args
        self.state = board_state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        self.children = []
        self.expandable_moves = game.get_valid_moves(board_state)

        self.visit_count = 0
        self.value_sum = 0

    def get_player(self):
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
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = Board()
                child_state.pieces = self.state.pieces
                child_state = self.game.get_next_state(child_state, 1, action)
                child_state = self.game.change_perspective(child_state, player=-1)

                child = Node(self.game, self.args, board_state=child_state, parent=self,
                             action_taken=action, prior=prob)
                self.children.append(child)

    def simulate(self):
        value = self.game.get_game_ended(self.state, self.get_player())
        value = self.game.get_opponent_value(value)

        if value:
            return value

        rollout_state = Board()
        rollout_state.pieces = self.state.pieces
        rollout_player = 1
        while True:
            valid_moves = self.game.get_valid_moves(rollout_state)
            action = np.random.choice(np.where(valid_moves == 1)[0])
            rollout_state = self.game.get_next_state(rollout_state, rollout_player, action)
            value = self.game.get_game_ended(rollout_state, rollout_player)
            if value:
                if rollout_player == -1:
                    value = self.game.get_opponent_value(value)
                return value

            rollout_player = self.game.get_opponent(rollout_player)

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = self.game.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)

