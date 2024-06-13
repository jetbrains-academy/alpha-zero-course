import unittest
from unittest.mock import MagicMock
import numpy as np
import torch

from task import AlphaMCTS

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe


class TestMCTSSearch(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe(Board())
        self.args = {'num_searches': 10, 'C': 1.4}
        self.board = self.game.get_board()

        # Configure the mock model to return a fixed policy and value
        self.mock_model = MagicMock(
            device=torch.device('cpu')
        )
        policy = torch.rand(1, 9)
        value = torch.tensor([[0.5]])
        self.mock_model.return_value = (policy, value)

    def test_search_action_probabilities(self):
        mcts = AlphaMCTS(self.game, self.args, self.mock_model)
        action_probs = mcts.search(self.board)

        # Check if action probabilities sum to 1
        self.assertAlmostEqual(np.sum(action_probs), 1, places=5,
                               msg="Check if action probabilities sum to 1")

        # Ensure that all action probabilities are non-negative
        self.assertTrue(np.all(action_probs >= 0),
                        msg="Ensure that all action probabilities are non-negative")


if __name__ == '__main__':
    unittest.main()
