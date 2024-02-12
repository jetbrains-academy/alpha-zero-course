import unittest
import torch

from task import ResNet


class MockGame:
    def __init__(self, size):
        self.size = size

    def get_action_size(self):
        return self.size ** 2


class TestResNet(unittest.TestCase):
    def setUp(self):
        self.game = MockGame(size=3)  # Assuming a 3x3 game board
        self.num_res_blocks = 5
        self.num_hidden = 32
        self.model = ResNet(self.game, self.num_res_blocks, self.num_hidden)

    def test_startBlock(self):
        # Create a mock input tensor
        input_tensor = torch.randn(1, 3, 3, 3)  # Batch size of 1, 3 channels, 3x3 size
        output = self.model.startBlock(input_tensor)
        # Check if the output has the expected shape
        self.assertEqual(output.shape, (1, self.num_hidden, 3, 3))

    def test_policyHead(self):
        # Assuming the policy head outputs a vector of action probabilities
        input_tensor = torch.randn(1, self.num_hidden, 3, 3)  # Input to the policy head
        output = self.model.policyHead(input_tensor)
        expected_output_size = self.game.get_action_size()
        # Check if the output size matches the game's action size
        self.assertEqual(output.shape[1], expected_output_size)

    def test_valueHead(self):
        # Assuming the value head outputs a single value representing the board evaluation
        input_tensor = torch.randn(1, self.num_hidden, 3, 3)  # Input to the value head
        output = self.model.valueHead(input_tensor)
        # Check if the output is a single value
        self.assertEqual(output.numel(), 1)
        # Also check if the output is between -1 and 1 (due to Tanh activation)
        self.assertTrue(1 >= output >= -1)


if __name__ == '__main__':
    unittest.main()
