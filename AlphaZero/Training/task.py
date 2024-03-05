import torch
import matplotlib.pyplot as plt

from TicTacToe.Game.Game import TicTacToe
from ResNetEstimator.Model.task import ResNet
from AlphaZero.SelfPlay.task import AlphaZero

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 2,
    'num_self_play_iterations': 50,
    'num_epochs': 4,
    'batch_size': 32,
    'temperature': 1.25,
}


def train():
    tictactoe = TicTacToe()

    model = ResNet(tictactoe, 4, 64)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
    alphaZero = AlphaZero(model, optimizer, tictactoe, args)

    alphaZero.learn()


if __name__ == '__main__':
    # Training
    train()

    # Playing
    model_num = args['num_iterations'] - 1  # Using latest iteration model

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

    print(value)
    print(state)
    print(tensor_state)
    print(policy)
    plt.bar(range(tictactoe.get_action_size()), policy)
    plt.show()
