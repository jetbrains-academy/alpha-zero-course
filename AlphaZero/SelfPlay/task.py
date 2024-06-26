import os
import random

import numpy as np
import torch

from tqdm import trange

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe
from ResNetEstimator.Model.task import ResNet
from AlphaMCTS.TreeSearch.task import AlphaMCTS


class AlphaZero:
    def __init__(self, model, optimizer, game, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = AlphaMCTS(game, args, model)

    def self_play_random(self):
        memory = []
        player = 1
        state = self.game.get_board().create_new_board()

        while True:
            neutral_state = self.game.change_perspective(state, player)
            action_probs = self.mcts.search(neutral_state)
            valid_moves = neutral_state.get_valid_moves()
            action_probs *= valid_moves
            action_probs /= np.sum(action_probs)

            memory.append((neutral_state, action_probs, player))

            action = np.random.choice(self.game.get_board().get_action_size(), p=action_probs)
            state = self.game.get_next_state(state, player, action)

            value = self.game.get_game_ended(state, player)

            if value:
                return_memory = []
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    return_memory.append((
                        hist_neutral_state.get_encoded_state(),
                        hist_action_probs,
                        hist_outcome
                    ))
                return return_memory

            player = self.game.get_opponent(player)

    def self_play(self):
        return self.self_play_random()

    def train(self, memory):
        raise NotImplemented

    def learn(self):
        for iteration in range(self.args['num_iterations']):
            memory = []

            self.model.eval()
            for self_play_iteration in trange(self.args['num_self_play_iterations']):
                memory += self.self_play()

            self.model.train()
            for epoch in trange(self.args['num_epochs']):
                self.train(memory)

            if not os.path.exists(f"models/"):
                os.makedirs(f"models/")
            torch.save(self.model.state_dict(), f"models/model_{iteration}.pt")
            torch.save(self.optimizer.state_dict(), f"models/optimizer_{iteration}.pt")


args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 1,
    'num_self_play_iterations': 10,
    'num_epochs': 0,
    'temperature': 1.25,
}

if __name__ == '__main__':
    tictactoe = TicTacToe(Board())
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = ResNet(tictactoe, 4, 64, device=device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

    alphaZero = AlphaZero(model, optimizer, tictactoe, args)
    alphaZero.learn()
