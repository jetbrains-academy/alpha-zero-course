import unittest
import numpy as np

from task import BoardC4, EMPTY, WHITE, BLACK


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = BoardC4()

    def test_init(self):
        """Test board initialization"""
        self.assertEqual(self.board._num_rows, 6)
        self.assertEqual(self.board._num_cols, 7)
        self.assertTrue(np.all(self.board.pieces == EMPTY))

    def test_is_win_horizontal(self):
        """Test horizontal win"""
        for row in range(6):
            board = BoardC4()
            for col in range(4):
                board.execute_move(col, WHITE)
            self.assertTrue(board.is_win(WHITE))

    def test_is_win_vertical(self):
        """Test vertical win"""
        board = BoardC4()
        for row in range(4):
            board.execute_move(0, BLACK)
        self.assertTrue(board.is_win(BLACK))

    def test_is_win_positive_diagonal(self):
        """Test positive diagonal win"""
        board = BoardC4()
        for i in range(4):
            for j in range(i):
                board.execute_move(i, WHITE)  # Fill columns to create diagonal setup
            board.execute_move(i, BLACK)
        self.assertTrue(board.is_win(BLACK))

    def test_is_win_negative_diagonal(self):
        """Test negative diagonal win"""
        board = BoardC4()
        for i in range(4):
            for j in range(3 - i):
                board.execute_move(3 + i, WHITE)  # Fill columns to create diagonal setup
            board.execute_move(3 + i, BLACK)
        self.assertTrue(board.is_win(BLACK))

    def test_execute_move(self):
        """Test executing a move updates the board correctly"""
        self.board.execute_move(0, WHITE)
        self.assertEqual(self.board[5, 0], WHITE)  # Assuming 0-indexed bottom row
        self.board.execute_move(0, BLACK)
        self.assertEqual(self.board[4, 0], BLACK)


if __name__ == '__main__':
    unittest.main()
