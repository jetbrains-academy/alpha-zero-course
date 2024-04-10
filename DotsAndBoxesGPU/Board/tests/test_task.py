import unittest
import numpy as np

from task import BoardDandB, EMPTY, WHITE, BLACK


class TestBoardDandB(unittest.TestCase):
    def setUp(self):
        self.board = BoardDandB()

    def test_init(self):
        """Test board initialization"""
        expected_rows = 5
        expected_cols = 5
        self.assertEqual(self.board._num_rows, expected_rows)
        self.assertEqual(self.board._num_cols, expected_cols)
        self.assertTrue(np.all(self.board.pieces == EMPTY))

    def test_increase_score(self):
        """Test score increase for both players"""
        self.board.increase_score(1, WHITE)
        self.assertEqual(self.board.pieces[0, -1], 1)
        self.board.increase_score(1, BLACK)
        self.assertEqual(self.board.pieces[1, -1], 1)

    def test_toggle_pass(self):
        """Test toggling the pass state"""
        self.board.toggle_pass(True)
        self.assertEqual(self.board.is_pass_on(), True)
        self.board.toggle_pass(False)
        self.assertEqual(self.board.is_pass_on(), False)

    def test_has_valid_moves(self):
        """Test if the board has any valid moves left"""
        # Initially, should have valid moves
        self.assertTrue(self.board.has_valid_moves())

        # Simulate a full board (except for the score and pass cells),
        # should have no valid moves
        self.board.pieces[:, :] = 1
        self.assertFalse(self.board.has_valid_moves())

    def test_get_valid_moves(self):
        """Test retrieval of valid moves"""
        # Initially, all moves are valid except the last one (pass)
        valid_moves_initial = self.board.get_valid_moves()
        self.assertFalse(valid_moves_initial[-1])
        self.assertTrue(np.all(valid_moves_initial[:-1]))

        # After toggling pass, only the last move (pass) is valid
        self.board.toggle_pass(True)
        valid_moves_pass = self.board.get_valid_moves()
        self.assertTrue(valid_moves_pass[-1])
        self.assertFalse(np.any(valid_moves_pass[:-1]))

    def test_execute_move(self):
        """Test executing a move"""
        player = WHITE
        action = 0  # Assume an action that's valid at the beginning of the game
        self.board.execute_move(player, action)
        # Verify a piece is placed correctly, and score or pass state is updated appropriately
        # This needs to be tailored based on the expected game logic after executing the action

        # Also, test for invalid action execution
        with self.assertRaises(AssertionError):
            self.board.execute_move(player, action)  # Trying to place where a piece already exists


if __name__ == '__main__':
    unittest.main()
