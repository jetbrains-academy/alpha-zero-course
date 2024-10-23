import os

import torch

from DotsAndBoxes.Board.task import BoardDandB
from DotsAndBoxes.Backend.task import Backend
from DotsAndBoxes.FlaskApp.task import args, device, FlaskApp
from ResNetEstimator.Model.task import ResNet
from AlphaZero.Training.task import AlphaZeroTrainer
from DotsAndBoxes.Game.task import DotsAndBoxes


def train():
    dots_boxes = DotsAndBoxes(BoardDandB())
    model = ResNet(dots_boxes, 4, 64, device=device)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=0.001, weight_decay=0.0001
    )

    alphaZero = AlphaZeroTrainer(model, optimizer, dots_boxes, args)
    alphaZero.learn()
    return model


def main():
    model = ResNet(DotsAndBoxes(BoardDandB()), 4, 64, device=device)
    model_num = args['num_iterations'] - 1
    filename = f'models/model_{model_num}.pt'
    if os.path.exists(filename):
        model.load_state_dict(torch.load(filename, map_location=device))
    else:
        model = train()
    model.eval()
    game_backend = Backend(BoardDandB())
    game_backend.agent = model
    game_backend.agent_play = True
    game_backend.player2 = "AlphaZero"
    app = FlaskApp(game_backend)
    app.run()


if __name__ == '__main__':
    main()
