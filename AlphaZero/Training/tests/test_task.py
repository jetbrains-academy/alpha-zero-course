import unittest
import torch

from AlphaZero.Training.task import args
from ResNetEstimator.Model.task import ResNet
from TicTacToe.Game.Game import TicTacToe


model_num = args['num_iterations']-1


class TestCase(unittest.TestCase):

    def test_occupied(self):
        # Playing
        tictactoe = TicTacToe()
        state = tictactoe.get_init_board()
        state = tictactoe.get_next_state(state, 1, 2)
        state = tictactoe.get_next_state(state, -1, 7)

        encoded_state = tictactoe.get_encoded_state(state)

        tensor_state = torch.tensor(encoded_state).unsqueeze(0)

        model = ResNet(tictactoe, 4, 64)
        model.load_state_dict(torch.load('model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        self.assertLess(policy[2], 0.01, "Model shouldn't consider for the move occupied cells")
        self.assertLess(policy[7], 0.01, "Model shouldn't consider for the move occupied cells")

    def test_win_move(self):
        tictactoe = TicTacToe()
        state = tictactoe.get_init_board()
        state = tictactoe.get_next_state(state, 1, 0)
        state = tictactoe.get_next_state(state,       -1, 1)
        state = tictactoe.get_next_state(state, 1, 2)
        state = tictactoe.get_next_state(state,       -1, 3)
        state = tictactoe.get_next_state(state, 1, 4)
        state = tictactoe.get_next_state(state,       -1, 5)

        encoded_state = tictactoe.get_encoded_state(state)

        tensor_state = torch.tensor(encoded_state).unsqueeze(0)

        model = ResNet(tictactoe, 4, 64)
        model.load_state_dict(torch.load('model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        for i in range(6):
            self.assertLess(policy[i], 0.01, "Model shouldn't consider for the move occupied cells")
        self.assertLess(policy[7], 0.01, "Model shouldn't consider not winning move at this board state")
        win_move = max(policy[6], policy[8])
        self.assertGreater(win_move, 0.85, "Model should choose only one of the winning move with high confidence")

    def test_save_move(self):
        tictactoe = TicTacToe()
        state = tictactoe.get_init_board()
        state = tictactoe.get_next_state(state, 1, 0)
        state = tictactoe.get_next_state(state,       -1, 2)
        state = tictactoe.get_next_state(state, 1, 1)
        state = tictactoe.get_next_state(state,       -1, 5)

        encoded_state = tictactoe.get_encoded_state(state)

        tensor_state = torch.tensor(encoded_state).unsqueeze(0)

        model = ResNet(tictactoe, 4, 64)
        model.load_state_dict(torch.load('model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        for i in (0, 1, 2, 5):
            self.assertLess(policy[i], 0.01, "Model shouldn't consider for the move occupied cells")
        self.assertGreater(policy[8], 0.7, "Model should prevent opponent from winning on this turn.")
