import unittest
import numpy as np

from task import BoardC4, EMPTY, WHITE, BLACK


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = BoardC4()

    def test_init(self):
        """Test board initialization"""
        self.assertEqual(self.board._num_rows, 6,
                         msg='By default num_rows should be 6')
        self.assertEqual(self.board._num_cols, 7,
                         msg='By default num_cols should be 7')
        self.assertTrue(np.all(self.board._pieces == EMPTY),
                        msg='All pieces should be EMPTY')

    def test_is_win_horizontal(self):
        """Test horizontal win"""
        for row in range(6):
            board = BoardC4()
            for col in range(4):
                board.execute_move(WHITE, col)
            self.assertTrue(board.is_win(WHITE),
                            msg=f'WHITE player should win in horizontal')

    def test_is_win_positive_diagonal(self):
        """Test positive diagonal win"""
        board = BoardC4()
        for i in range(4):
            for j in range(i):
                board.execute_move(WHITE, i)  # Fill columns to create diagonal setup
            board.execute_move(BLACK, i)
        self.assertTrue(board.is_win(BLACK),
                        msg=f'BLACK player should win in positive diagonal')

    def test_execute_move(self):
        """Test executing a move updates the board correctly"""
        self.board.execute_move(WHITE, 0)
        self.assertEqual(WHITE, self.board[5, 0],  # Assuming 0-indexed top row
                         msg="Test executing a move updates the board correctly")
        self.board.execute_move(BLACK, 0)
        self.assertEqual(BLACK, self.board[4, 0],
                         msg="Test executing a move updates the board correctly")


if __name__ == '__main__':
    unittest.main()
