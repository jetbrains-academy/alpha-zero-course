import numpy as np
import unittest

from unittest.mock import MagicMock, patch
from DotsAndBoxesGPU.Board.task import BoardDandB

from task import DotsAndBoxes


class TestDotsAndBoxes(unittest.TestCase):
    def setUp(self):
        self.game = DotsAndBoxes(3, 3)

    def test_get_valid_moves(self):
        """Test getting valid moves"""
        board_instance = BoardDandB(3, 3)
        expected = board_instance.get_valid_moves()

        valid_moves = self.game.get_valid_moves(1)
        self.assertTrue(np.all(valid_moves == expected))

    @patch('DotsAndBoxesGPU.Board.task.BoardDandB')
    def test_game_ended(self, mock_board):
        """Test game ended conditions"""
        mock_board_instance = mock_board.return_value
        mock_board_instance.has_valid_moves.return_value = False
        mock_board_instance.pieces = np.array([[0, 0], [0, 0], [0, 1]])

        # Simulate a draw
        game_ended = self.game.get_game_ended(mock_board_instance, 1)
        self.assertEqual(game_ended, 0)  # Assuming the game ends in a draw under certain conditions


if __name__ == '__main__':
    unittest.main()
