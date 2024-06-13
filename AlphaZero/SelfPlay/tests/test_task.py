import unittest
from unittest.mock import patch
import numpy as np
import torch

from task import AlphaZero

from ResNetEstimator.Model.task import ResNet
from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe


class TestAlphaZero(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe(Board())
        self.model = ResNet(self.game, 4, 64, device=torch.device('cpu'))
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001, weight_decay=1e-4)
        self.args = {
            'C': 2,
            'num_searches': 60,
            'num_iterations': 2,
            'num_self_play_iterations': 10,
            'num_epochs': 3,
            'temperature': 1.25,
        }
        self.alphaZero = AlphaZero(self.model, self.optimizer, self.game, self.args)

    def test_self_play_memory_structure(self):
        memory = self.alphaZero.self_play_random()

        # Check if memory is not empty
        self.assertTrue(len(memory) > 0, msg="Check if memory is not empty")

        # Validate the structure of memory entries
        for state, probs, outcome in memory:
            self.assertIsInstance(state, np.ndarray, msg="Check if state is ndarray")
            self.assertEqual(state.shape, (3, 3, 3), msg="Check if state has shape (3,3)")
            self.assertIsInstance(probs, np.ndarray, msg="Check if probs is ndarray")
            self.assertEqual(probs.shape, (9,), msg="Check if probs has shape (9,)")

    @patch('torch.save')
    @patch('task.AlphaZero.train')
    @patch('task.AlphaZero.self_play')
    def test_learn(self, mock_self_play, mock_train, mock_torch_save):
        """Test the learn method orchestrates self play, training and saving models."""
        # Setup mock returns
        mock_self_play.return_value = [('state', 'probs', 'outcome')]
        memory = [('state', 'probs', 'outcome')] * 10

        # Call the learn method
        self.alphaZero.learn()

        # Check that self_play is called the correct number of times
        self.assertEqual(mock_self_play.call_count, self.args['num_self_play_iterations'] * self.args['num_iterations'])

        # Check that train is called the correct number of times
        mock_train.assert_called_with(memory)

        # Ensure model saving happens the correct number of times
        expected_num_saves = self.args['num_iterations']
        self.assertEqual(mock_torch_save.call_count, expected_num_saves * 2)  # For model and optimizer each

        # Check arguments passed to torch.save
        model_save_calls = [call[0] for call in mock_torch_save.call_args_list if 'model_' in call[0][1]]
        optimizer_save_calls = [call[0] for call in mock_torch_save.call_args_list if 'optimizer_' in call[0][1]]
        self.assertEqual(len(model_save_calls), expected_num_saves)
        self.assertEqual(len(optimizer_save_calls), expected_num_saves)


if __name__ == '__main__':
    unittest.main()
