import torch

from TicTacToe.GameImplementation.Game import TicTacToe
from ResNetEstimator.Model.task import ResNet
from AlphaZero.SelfPlay.task import AlphaZero

tictactoe = TicTacToe()

model = ResNet(tictactoe, 4, 64)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 2,
    'num_self_play_iterations': 50,
    'num_epochs': 4,
    'batch_size': 32,
    'temperature': 1.25,
}

alphaZero = AlphaZero(model, optimizer, tictactoe, args)
alphaZero.learn()
