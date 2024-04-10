import math
from abc import ABC
import numpy as np

from GameInterface import Game
from TicTacToe.Board.task import Board


class TicTacToe(Game, ABC):
    def __init__(self, num_rows=3, num_cols=3):
        self._board = Board(num_rows, num_cols)

    def get_board(self):
        return self._board

    def get_next_state(self, board, player, action):
        board.execute_move(player, action)
        return board

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
        # return state if player==1, else return -state if player==-1
        return player * self._board

    def get_opponent(self, player):
        # Return the opponent player
        return -player

    def get_opponent_value(self, value):
        return value if math.isclose(value, 1e-4) else -value

    def change_perspective(self, board, player):
        board_changed = self._board.create_new_board()
        board_changed.pieces = board.pieces.copy() * player
        return board_changed
