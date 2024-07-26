import os

import torch

from DotsAndBoxes.Board.task import BoardDandB
from DotsAndBoxes.Visualization.task import DotsAndBoxesVisualization
from ResNetEstimator.Model.task import ResNet
from AlphaZero.Training.task import AlphaZeroTrainer
from DotsAndBoxes.Game.task import DotsAndBoxes

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 3,
    'num_self_play_iterations': 100,
    'num_epochs': 25,
    'temperature': 1.25,
    'batch_size': 64,
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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cpu":
        game_instance = DotsAndBoxesVisualization(BoardDandB())
    else:
        # for training on GPU without GUI
        game_instance = DotsAndBoxes(BoardDandB())

    model = ResNet(game_instance, 4, 64, device=device)
    model_num = args['num_iterations'] - 1
    filename = f'models/model_{model_num}.pt'

    if os.path.exists(filename):
        model.load_state_dict(torch.load(filename, map_location=device))
    else:
        model = train()
    model.eval()

    # the inference is on CPU with GUI
    if device.type == "cpu":
        game_instance.agent = model
        game_instance.agent_play = True
        game_instance.player2 = "AlphaZero"
        game_instance.run()
