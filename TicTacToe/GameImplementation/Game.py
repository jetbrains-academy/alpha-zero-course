from abc import ABC

import numpy as np
from GameInterface import Game

from TicTacToe.Board.task import Board

class TicTacToe(Game, ABC):
    def __init__(self, size=3):
        self.size = size  # Size of the TicTacToe board
        self.board = Board(self.size)

    def get_init_board(self):
        return self.board

    def get_board_size(self):
        return self.size, self.size

    def get_action_size(self):
        return self.size ** 2

    def get_next_state(self, board, player, action):
        move = action // self.size, action % self.size
        board.execute_move(move, player)
        return board

    def get_valid_moves(self, board, player=1):
        # Returns a flat array indicating valid moves
        return (board.pieces.reshape(-1) == 0).astype(np.uint8)

    def get_game_ended(self, board, player):
        if board.is_win(player):
            return 1
        if board.is_win(-player):
            return -1
        if board.has_legal_moves():
            return 0
        # draw has a very little positive reward
        return 1e-4

    def get_canonical_form(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    def string_representation(self, board):
        return board.tostring()

    def get_opponent(self, player):
        # Return the opponent player
        return -player

    def get_opponent_value(self, value):
        return -value

    def change_perspective(self, board, player):
        board_changed = Board()
        board_changed.pieces = board.pieces * player
        return board_changed

    def get_encoded_state(self, board):
        encoded_state = np.stack(
            (board.pieces == -1, board.pieces == 0, board.pieces == 1)
        ).astype(np.float32)

        return encoded_state

