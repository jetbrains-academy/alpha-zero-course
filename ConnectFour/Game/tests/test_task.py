import unittest
import numpy as np

from task import ConnectFour


class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.game = ConnectFour()

    def test_init(self):
        """Test game initialization"""
        self.assertEqual(self.game.num_rows, 6)
        self.assertEqual(self.game.num_cols, 7)
        self.assertTrue(np.all(self.game.get_board().pieces == 0))

    def test_valid_moves(self):
        """Test getting valid moves on an empty board"""
        valid_moves = self.game.get_valid_moves(self.game.get_board())
        self.assertTrue(np.all(valid_moves == 1))

    def test_game_end_conditions(self):
        """Test game end conditions: win, lose, draw"""
        # Simulate a win condition for player 1
        for _ in range(4):
            self.game.get_board().execute_move(0, 1)
        self.assertEqual(self.game.get_game_ended(self.game.get_board(), 1), 1)

        # Reset and simulate a win for player -1
        self.setUp()
        for _ in range(4):
            self.game.get_board().execute_move(1, -1)
        self.assertEqual(self.game.get_game_ended(self.game.get_board(), -1), 1)

    def test_change_perspective(self):
        """Test changing the board's perspective"""
        self.game.get_board().execute_move(0, 1)  # Player 1 move
        changed_board = self.game.change_perspective(self.game.get_board(), -1)
        self.assertEqual(changed_board.pieces[5, 0], -1)  # Ensure the perspective is inverted

    def test_get_encoded_state(self):
        """Test encoding the board state"""
        self.game.get_board().execute_move(0, 1)  # Player 1 move
        encoded_state = self.game.get_encoded_state(self.game.get_board())
        # print(encoded_state)
        self.assertTrue(encoded_state.shape == (3, 6, 7))
        self.assertTrue(np.all(encoded_state[2, 5, 0] == 1))


if __name__ == '__main__':
    unittest.main()
