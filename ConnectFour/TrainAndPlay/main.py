import os

import numpy as np
import torch

from ConnectFour.Board.task import BoardC4
from ResNetEstimator.Model.task import ResNet
from AlphaZero.Training.task import AlphaZeroTrainer
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 2,
    'num_self_play_iterations': 250,
    'num_epochs': 4,
    'temperature': 1.25,
    'batch_size': 32,
}

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

def train():
    connect4 = TicTacToe(BoardC4())
    model = ResNet(connect4, 4, 64, device=device)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=0.001, weight_decay=0.0001
    )

    alphaZero = AlphaZeroTrainer(model, optimizer, connect4, args)
    alphaZero.learn()
    return model


def play(round, model):
    player = round.player

    is_playing = True
    while is_playing:
        if player == 1:
            round.print_game_layout()
            action = int(input())
        else:
            encoded_state = round.instance_of_game.get_board().get_encoded_state()
            tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(device)

            policy, value = model(tensor_state)
            policy = (
                torch.softmax(policy, axis=1)
                .squeeze(0).detach().cpu().numpy()
            )
            valid_moves = round.instance_of_game.get_board().get_valid_moves()
            policy *= valid_moves
            policy /= np.sum(policy)
            action = np.argmax(policy)

        is_playing = round.play_game(action)
        player = round.instance_of_game.get_opponent(player)


def main():
    connect4 = TicTacToe(BoardC4())
    round = Round(connect4)
    model = ResNet(round.instance_of_game, 4, 64, device=device)
    model_num = args['num_iterations'] - 1
    filename = f'./models/model_{model_num}.pt'
    if os.path.exists(filename):
        model.load_state_dict(torch.load(filename))
    else:
        model = train()
    model.eval()
    play(round, model)


if __name__ == '__main__':
    main()
