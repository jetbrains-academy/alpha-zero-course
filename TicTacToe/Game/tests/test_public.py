import unittest
import numpy as np

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe


class TestCase(unittest.TestCase):
    def test_init(self):
        board = Board(4, 4)
        tictactoe = TicTacToe(board)
        self.assertEqual(16, tictactoe.get_board()._pieces.size, msg="Board(4,4) should have 16 cells")

    def test_next_state(self):
        board = Board()
        tictactoe = TicTacToe(board)
        board = tictactoe.get_next_state(board, 1, 4)
        self.assertEqual(1, board[1, 1],
                         msg="get_next_state() after action 4 for player 1 should return board where [1,1] element == 1")

    def test_get_valid_moves(self):
        board = Board()
        tictactoe = TicTacToe(board)
        tictactoe.get_next_state(board, 1, 0)
        tictactoe.get_next_state(board, -1, 1)
        tictactoe.get_next_state(board, 1, 2)
        valid_moves = tictactoe.get_valid_moves()
        actual_board = list(valid_moves)
        expected_board = [0, 0, 0, 1, 1, 1, 1, 1, 1]
        self.assertEqual(expected_board, actual_board,
                         msg="get_valid_moves() returns wrong list after players made their actions to 1st row")

    def test_change_perspective(self):
        board = Board()
        tictactoe = TicTacToe(board)
        board._pieces = np.array([[1, 0, 1],
                                  [0, 0, 0],
                                  [-1, 0, -1]])
        new_board = tictactoe.change_perspective(board, -1)
        actual = str(new_board)
        expected = 'O-O\n---\nX-X\n'
        self.assertEqual(expected,
                         actual,
                         msg="wrong change_perspective() work")
