import unittest
import numpy as np

from task import BoardDandB, EMPTY, WHITE, BLACK


class TestBoardDandB(unittest.TestCase):
    def setUp(self):
        self.board = BoardDandB()

    def test_init(self):
        """Test board initialization"""
        expected_rows = 3
        expected_cols = 3
        self.assertEqual(self.board._num_rows, expected_rows,
                         msg="Number of rows is not as expected")
        self.assertEqual(self.board._num_cols, expected_cols,
                         msg="Number of columns is not as expected")
        self.assertTrue(np.all(self.board.pieces == EMPTY),
                        msg="Board is not initialized correctly")

    def test_increase_score(self):
        """Test score increase for both players"""
        self.board.increase_score(1, WHITE)
        self.assertEqual(self.board.pieces[0, -1], 1,
                         msg="Score for player 1 is not increased correctly")
        self.board.increase_score(1, BLACK)
        self.assertEqual(self.board.pieces[1, -1], 1,
                         msg="Score for player 2 is not increased correctly")

    def test_toggle_pass(self):
        """Test toggling the pass state"""
        self.board.toggle_pass(True)
        self.assertEqual(self.board.is_pass_on(), True,
                         msg="Pass state is not toggled correctly")
        self.board.toggle_pass(False)
        self.assertEqual(self.board.is_pass_on(), False,
                         msg="Pass state is not toggled correctly")

    def test_has_valid_moves(self):
        """Test if the board has any valid moves left"""
        # Initially, should have valid moves
        self.assertTrue(self.board.has_valid_moves(),
                        msg="Board should have valid moves initially")

        # Simulate a full board (except for the score and pass cells),
        # should have no valid moves
        self.board.pieces[:, :] = 1
        self.assertFalse(self.board.has_valid_moves(),
                         msg="Board should not have valid moves after filling all cells")

    def test_get_valid_moves(self):
        """Test retrieval of valid moves"""
        # Initially, all moves are valid except the last one (pass)
        valid_moves_initial = self.board.get_valid_moves()
        self.assertFalse(valid_moves_initial[-1],
                         msg="Last move should not be valid initially")
        self.assertTrue(np.all(valid_moves_initial[:-1]),
                        msg="All other moves should be valid initially")

        # After toggling pass, only the last move (pass) is valid
        self.board.toggle_pass(True)
        valid_moves_pass = self.board.get_valid_moves()
        self.assertTrue(valid_moves_pass[-1],
                        msg="Last move should be valid after toggling pass")
        self.assertFalse(np.any(valid_moves_pass[:-1]),
                         msg="All other moves should not be valid after toggling pass")

    def test_execute_move(self):
        """Test executing a move"""
        player = WHITE
        action = 0  # Assume an action that's valid at the beginning of the game
        self.board.execute_move(player, action)
        # Verify a piece is placed correctly, and score or pass state is updated appropriately
        # This needs to be tailored based on the expected game logic after executing the action

        # Also, test for invalid action execution
        with self.assertRaises(AssertionError, msg="Pass should not be allowed as a move"):
            self.board.execute_move(player, action)  # Trying to place where a piece already exists


if __name__ == '__main__':
    unittest.main()
