import unittest
from unittest.mock import MagicMock
import numpy as np
import torch

# Assuming your MCTS and Node classes are in specific files
from task import AlphaMCTS

from TicTacToe.Board.task import Board


class TestMCTSSearch(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.args = {'num_searches': 10, 'C': 1.4}
        self.mock_model = MagicMock()

        # Configure the mock game
        self.mock_game.get_action_size.return_value = 9  # For a 3x3 board
        self.mock_game.get_valid_moves.return_value = np.ones(9)
        self.mock_game.get_game_ended.return_value = 0
        encoded_state = np.zeros((3, 3))
        self.board = Board(3, 3)
        self.board.pieces = encoded_state
        self.mock_game.get_encoded_state.return_value = encoded_state
        self.mock_game.get_opponent_value.side_effect = lambda x: -x

        # Configure the mock model to return a fixed policy and value
        policy = torch.rand(1, 9)
        value = torch.tensor([[0.5]])
        self.mock_model.return_value = (policy, value)

    def test_search_action_probabilities(self):
        mcts = AlphaMCTS(self.mock_game, self.args, self.mock_model)
        action_probs = mcts.search(self.board)

        # Check if action probabilities sum to 1
        self.assertAlmostEqual(np.sum(action_probs), 1, places=5,
                               msg="Check if action probabilities sum to 1")

        # Ensure that all action probabilities are non-negative
        self.assertTrue(np.all(action_probs >= 0),
                        msg="Ensure that all action probabilities are non-negative")


if __name__ == '__main__':
    unittest.main()
