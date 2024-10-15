import unittest
from unittest.mock import MagicMock
import numpy as np
import torch

from AlphaZero.Training.task import args

from ResNetEstimator.Model.task import ResNet
from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe

from task import AlphaZeroTrainer

model_num = args['num_iterations'] - 1


class TestAlphaZeroTrainer(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe(Board())
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = ResNet(self.game, 4, 64, device=self.device)
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
            return_value=np.ones(self.game.get_board().get_action_size()) /
                                 self.game.get_board().get_action_size()
        )
        self.game.change_perspective = lambda board, player: board
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
            (np.ones((3, 3, 3)), np.ones(self.game.get_board().get_action_size()), 1)
        ]
        self.alphaZero.train(memory)
        for name, param in self.model.named_parameters():
            self.assertFalse(
                torch.equal(initial_weights[name], param),
                msg=f"Parameter {name} did not update."
            )

    def test_occupied(self):
        # Playing
        tictactoe = TicTacToe(Board())
        state = tictactoe.get_board()
        state = tictactoe.get_next_state(state, 1, 2)
        state = tictactoe.get_next_state(state, -1, 7)

        encoded_state = state.get_encoded_state()
        tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(self.device)

        model = self.model
        model.load_state_dict(torch.load('./models/model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        self.assertLess(policy[2], 0.05, "Model shouldn't consider for the move occupied cells")
        self.assertLess(policy[7], 0.05, "Model shouldn't consider for the move occupied cells")

    def test_win_move(self):
        tictactoe = TicTacToe(Board())
        state = tictactoe.get_board()
        state = tictactoe.get_next_state(state, 1, 0)
        state = tictactoe.get_next_state(state,       -1, 1)
        state = tictactoe.get_next_state(state, 1, 2)
        state = tictactoe.get_next_state(state,       -1, 3)
        state = tictactoe.get_next_state(state, 1, 4)
        state = tictactoe.get_next_state(state,       -1, 5)

        encoded_state = state.get_encoded_state()

        tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(self.device)

        model = self.model
        model.load_state_dict(torch.load('./models/model_{}.pt'.format(model_num)))
        model.eval()

        policy, _ = model(tensor_state)
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        for i in range(6):
            self.assertLess(policy[i], 0.15, "Model shouldn't consider for the move occupied cells")
        self.assertLess(policy[7], 0.15, "Model shouldn't consider not winning move at this board state")
        win_move = max(policy[6], policy[8])
        self.assertGreater(win_move, 0.5, "Model should choose only one of the winning move with high confidence")

    def test_save_move(self):
        tictactoe = TicTacToe(Board())
        state = tictactoe.get_board()
        state = tictactoe.get_next_state(state, 1, 0)
        state = tictactoe.get_next_state(state,       -1, 4)
        state = tictactoe.get_next_state(state, 1, 1)
        state = tictactoe.get_next_state(state,       -1, 2)

        encoded_state = state.get_encoded_state()

        tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(self.device)

        model = self.model
        model.load_state_dict(torch.load('./models/model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)
        for i in (0, 1, 2, 4):
            self.assertLess(policy[i], 0.05, "Model shouldn't consider for the move occupied cells")
        self.assertGreater(policy[6], 0.5, "Model should prevent opponent from winning on this turn.")

    def test_hard_move(self):
        tictactoe = TicTacToe(Board())
        state = tictactoe.get_board()
        state = tictactoe.get_next_state(state, 1, 0)
        state = tictactoe.get_next_state(state,       -1, 2)
        state = tictactoe.get_next_state(state, 1, 1)
        state = tictactoe.get_next_state(state,       -1, 5)

        encoded_state = state.get_encoded_state()

        tensor_state = torch.tensor(encoded_state).unsqueeze(0)

        model = self.model
        model.load_state_dict(torch.load('./models/model_{}.pt'.format(model_num)))
        model.eval()

        policy, value = model(tensor_state)
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        print('Field:')
        print(state)
        print("Policy:", policy)


if __name__ == '__main__':
    unittest.main()
