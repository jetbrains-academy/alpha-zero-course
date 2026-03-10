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

    def test_is_win_vertical(self):
        """Test vertical win"""
        board = BoardC4()
        for row in range(4):
            board.execute_move(BLACK, 0)
        self.assertTrue(board.is_win(BLACK),
                        msg=f'BLACK player should win in vertical')

    def test_is_win_positive_diagonal(self):
        """Test positive diagonal win"""
        board = BoardC4()
        for i in range(4):
            for j in range(i):
                board.execute_move(WHITE, i)  # Fill columns to create diagonal setup
            board.execute_move(BLACK, i)
        self.assertTrue(board.is_win(BLACK),
                        msg=f'BLACK player should win in positive diagonal')

    def test_is_win_negative_diagonal(self):
        """Test negative diagonal win"""
        board = BoardC4()
        for i in range(4):
            for j in range(3 - i):
                board.execute_move(WHITE, 3 + i)  # Fill columns to create diagonal setup
            board.execute_move(BLACK, 3 + i)
        self.assertTrue(board.is_win(BLACK),
                        msg=f'BLACK player should win in negative diagonal')

    def test_execute_move(self):
        """Test executing a move updates the board correctly"""
        self.board.execute_move(WHITE, 0)
        self.assertEqual(WHITE, self.board[5, 0],  # Assuming 0-indexed top row
                         msg="Test executing a move updates the board correctly")
        self.board.execute_move(BLACK, 0)
        self.assertEqual(BLACK, self.board[4, 0],
                         msg="Test executing a move updates the board correctly")


    def test_get_valid_moves_returns_binary_mask_on_empty_board(self):
        """get_valid_moves should return a uint8 binary mask, not a list of columns"""
        expected = np.ones(self.board._num_cols, dtype=np.uint8)
        actual = self.board.get_valid_moves()

        self.assertIsInstance(
            actual, np.ndarray,
            msg="get_valid_moves should return numpy.ndarray"
        )
        self.assertEqual(
            actual.dtype, np.uint8,
            msg="get_valid_moves should return np.uint8 mask"
        )
        np.testing.assert_array_equal(
            actual, expected,
            err_msg="On empty board all columns should be valid"
        )

    def test_get_valid_moves_marks_full_column_as_invalid(self):
        """A full column should be marked with 0 in valid moves mask"""
        for _ in range(self.board._num_rows):
            self.board.execute_move(WHITE, 0)

        expected = np.ones(self.board._num_cols, dtype=np.uint8)
        expected[0] = 0
        actual = self.board.get_valid_moves()

        self.assertIsInstance(
            actual, np.ndarray,
            msg="get_valid_moves should return numpy.ndarray"
        )
        self.assertEqual(
            actual.dtype, np.uint8,
            msg="get_valid_moves should return np.uint8 mask"
        )
        np.testing.assert_array_equal(
            actual, expected,
            err_msg="Filled column should be marked as invalid"
        )


if __name__ == '__main__':
    unittest.main()
