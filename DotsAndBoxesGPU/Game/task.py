import math
from abc import ABC
import numpy as np

from GameInterface import Game
from DotsAndBoxesGPU.Board.task import BoardDandB


class DotsAndBoxes(Game, ABC):
    def __init__(self, num_rows=3, num_cols=3):
        self._board = BoardDandB(num_rows, num_cols)

    def get_board(self):
        return self._board

    def get_next_state(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = board.copy()

        if action == b.get_action_size() - 1:
            b.pieces[2, -1] = 0
        else:
            b.execute_move(player, action)
        return b

    def get_valid_moves(self, player=1):
        return self._board.get_valid_moves()

    def get_game_ended(self, board, player):
        if board.is_win(player):
            return 1
        if board.is_win(-player):
            return -1
        if board.has_valid_moves():
            return 0
        # draw has a very little positive reward
        return 1e-4

    def get_canonical_form(self, player):
        board = self._board.copy()
        if player == -1:
            # swap score
            aux = board[0, -1]
            board[0, -1] = board[1, -1]
            board[1, -1] = aux
        return board

    def get_opponent(self, player):
        # Return the opponent player
        return -player

    def get_opponent_value(self, value):
        return value if math.isclose(value, 1e-4) else -value

    def change_perspective(self, board, player):
        board_changed = self._board.create_new_board()
        board_changed.pieces = board.pieces.copy() * player
        return board_changed
