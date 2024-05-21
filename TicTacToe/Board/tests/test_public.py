import unittest
import numpy as np
from TicTacToe.Board.task import Board


class TestCase(unittest.TestCase):

    def test_board_init(self):
        board = Board(2, 2)
        actual_board = str(board)
        expected_board = '--\n' * 2
        self.assertEqual(expected_board, actual_board, msg="Board with size 2 does not match")

    def test_set_get(self):
        board = Board()
        board[0, 0] = 1
        board[2, 1] = -1
        self.assertEqual(1, board[0, 0], msg="set after get for [0,0] gave wrong result")
        self.assertEqual(-1, board[2, 1], msg="set after get for [2,1] gave wrong result")

    def test_has_legal_moves(self):
        board = Board()
        self.assertTrue(board.has_valid_moves(), msg="Empty board should have legal moves")
        board._pieces = np.array([[1] * 3 for _ in range(3)])
        self.assertFalse(board.has_valid_moves(), msg="Full board shouldn't have legal moves")

    def test_execute_move(self):
        board = Board()
        board.execute_move(1, 0)
        self.assertEqual(1, board[0, 0], msg="execute_move() did not set the correct value at [0,0]")
        board.execute_move(-1,7)
        self.assertEqual(-1, board[2, 1], msg="execute_move() did not set the correct value at [2,1]")

    def test_get_encoded_state(self):
        board = Board()
        board._pieces = np.array([[1, 0, 1],
                                  [0, 0, 0],
                                  [-1, 0, -1]])
        expected = np.stack(
            (board._pieces == -1, board._pieces == 0, board._pieces == 1)
        ).astype(np.float32)
        actual = board.get_encoded_state()
        self.assertTrue(np.array_equal(expected, actual),
                        msg=f"get_encoded_state result for {board._pieces}\nshould be: {expected},\nbut got {actual}")
