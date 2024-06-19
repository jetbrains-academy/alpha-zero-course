import os

import numpy as np
import torch

from DotsAndBoxesGPU.Board.task import BoardDandB
from DotsAndBoxesGPU.Visualization.task import DotsAndBoxesVisualization
from ResNetEstimator.Model.task import ResNet
from AlphaZero.Training.task import AlphaZeroTrainer
from DotsAndBoxesGPU.Game.task import DotsAndBoxes

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 2,
    'num_self_play_iterations': 100,
    'num_epochs': 4,
    'temperature': 1.25,
    'batch_size': 32,
}


def train():
    dots_boxes = DotsAndBoxes(BoardDandB())
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(dots_boxes, 4, 64, device=device)

    optimizer = torch.optim.Adam(
        model.parameters(), lr=0.001, weight_decay=0.0001
    )

    alphaZero = AlphaZeroTrainer(model, optimizer, dots_boxes, args)
    alphaZero.learn()
    return model


if __name__ == '__main__':
    game_instance = DotsAndBoxesVisualization(BoardDandB())

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(game_instance, 4, 64, device=device)
    model_num = args['num_iterations'] - 1
    filename = f'model_{model_num}.pt'

    if os.path.exists(filename):
        model.load_state_dict(torch.load(filename))
    else:
        model = train()
    model.eval()

    game_instance.agent = model
    game_instance.agent_play = True
    game_instance.player2 = "AlphaZero"
    game_instance.run()
