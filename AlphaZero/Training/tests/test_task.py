import unittest
from unittest.mock import MagicMock
import numpy as np
import torch

from ResNetEstimator.Model.task import ResNet
from TicTacToe.Game.Game import TicTacToe

from task import AlphaZeroTrainer


class TestAlphaZeroTrainer(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()
        self.model = ResNet(self.game, 4, 64)
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=0.001
        )
        self.args = {
            'C': 2,
            'num_searches': 60,
            'num_iterations': 1,
            'num_self_play_iterations': 10,
            'num_epochs': 1,
            'temperature': 1.25,
            'batch_size': 32,
        }
        self.alphaZero = AlphaZeroTrainer(
            self.model, self.optimizer, self.game, self.args
        )

        # Mocking the MCTS and game methods for self_play
        self.alphaZero.mcts.search = MagicMock(
            return_value=np.ones(self.game.get_action_size()) /
                                 self.game.get_action_size()
        )
        self.game.change_perspective = MagicMock()
        self.game.get_next_state = MagicMock()
        self.game.get_game_ended = MagicMock(side_effect=[0, 0, 1])

    def test_self_play_returns_memory(self):
        memory = self.alphaZero.self_play()
        self.assertIsInstance(memory, list,
                              msg='Memory should be a list')
        self.assertGreater(len(memory), 0,
                           msg='Memory should be a nonempty list')
        # Check for the expected structure in memory entries
        for state, probs, outcome in memory:
            self.assertIsInstance(state, np.ndarray,
                                  msg='Check if state is ndarray')
            self.assertIsInstance(probs, np.ndarray,
                                  msg='Check if probs is ndarray')
            self.assertIsInstance(outcome, (int, float),
                                  msg='Check if outcome is int or float')

    def test_train_updates_model(self):
        initial_weights = {
            k: v.clone() for k, v in self.model.state_dict().items()
        }
        memory = [
            (np.ones((3, 3, 3)), np.ones(self.game.get_action_size()), 1)
        ]
        self.alphaZero.train(memory)
        for name, param in self.model.named_parameters():
            self.assertFalse(
                torch.equal(initial_weights[name], param),
                msg=f"Parameter {name} did not update."
            )


if __name__ == '__main__':
    unittest.main()
