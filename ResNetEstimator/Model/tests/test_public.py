import unittest
import torch

from task import ResNet

from TicTacToe.Board.task import Board


class MockGame:
    def __init__(self, num_rows, num_cols):
        self._board = Board(num_rows, num_cols)

    def get_action_size(self):
        return self._board.get_action_size()

    def get_board(self):
        return self._board


class TestResNet(unittest.TestCase):
    def setUp(self):
        self.game = MockGame(3, 3)  # Assuming a 3x3 game board
        self.num_res_blocks = 5
        self.num_hidden = 32
        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        self.model = ResNet(self.game, self.num_res_blocks, self.num_hidden, self.device)

    def test_startBlock(self):
        # Create a mock input tensor
        input_tensor = torch.randn(1, 3, 3, 3).to(self.device)  # Batch size of 1, 3 channels, 3x3 size
        output = self.model.startBlock(input_tensor)
        self.assertEqual(output.shape, (1, self.num_hidden, 3, 3),
                         msg="The output has unexpected shape.")

    def test_policyHead(self):
        # Assuming the policy head outputs a vector of action probabilities
        input_tensor = torch.randn(1, self.num_hidden, 3, 3).to(self.device)  # Input to the policy head
        output = self.model.policyHead(input_tensor)
        expected_output_size = self.game.get_action_size()
        self.assertEqual(output.shape[1], expected_output_size,
                         msg="The output size doesn't match the game's action size.")

    def test_valueHead(self):
        # Assuming the value head outputs a single value representing the board evaluation
        input_tensor = torch.randn(1, self.num_hidden, 3, 3).to(self.device)  # Input to the value head
        output = self.model.valueHead(input_tensor)
        self.assertEqual(output.numel(), 1,
                         msg="The output of value head is not a single value.")
        self.assertTrue(1 >= output >= -1,
                        msg="The output of value head is not between -1 and 1.")


if __name__ == '__main__':
    unittest.main()
