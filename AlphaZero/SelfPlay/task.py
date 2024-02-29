import random

import numpy as np
import torch

import torch.nn.functional as F
from tqdm import trange

from TicTacToe.Game.Game import TicTacToe
from ResNetEstimator.Model.task import ResNet
from AlphaMCTS.TreeSearch.task import MCTS


class AlphaZero:
    def __init__(self, model, optimizer, game, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = MCTS(game, args, model)

    def self_play(self):
        memory = []
        player = 1
        state = self.game.get_init_board()

        while True:
            neutral_state = self.game.change_perspective(state, player)
            action_probs = self.mcts.search(neutral_state)

            memory.append((neutral_state, action_probs, player))

            # print(action_probs)
            # if np.sum(action_probs) > 0:
            #     action_probs /= np.sum(action_probs)
            #     action = np.random.choice(self.game.get_action_size(), p=action_probs)
            #     state = self.game.get_next_state(state, player, action)

            temperature_action_probs = action_probs ** (1 / self.args['temperature'])
            print(action_probs, temperature_action_probs)
            if np.sum(temperature_action_probs) > 0:
                temperature_action_probs /= np.sum(temperature_action_probs)
                action = np.random.choice(self.game.get_action_size(), p=temperature_action_probs)
                state = self.game.get_next_state(state, player, action)

            value = self.game.get_game_ended(state, player)

            if value:
                returnMemory = []
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    returnMemory.append((
                        self.game.get_encoded_state(hist_neutral_state),
                        hist_action_probs,
                        hist_outcome
                    ))
                return returnMemory

            player = self.game.get_opponent(player)

    def train(self, memory):
        random.shuffle(memory)
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            sample = memory[batchIdx:batchIdx + self.args['batch_size']]
            state, policy_targets, value_targets = zip(*sample)

            state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(
                value_targets).reshape(-1, 1)

            state = torch.tensor(state, dtype=torch.float32)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32)
            value_targets = torch.tensor(value_targets, dtype=torch.float32)

            out_policy, out_value = self.model(state)

            policy_loss = F.cross_entropy(out_policy, policy_targets)
            value_loss = F.mse_loss(out_value, value_targets)
            loss = policy_loss + value_loss

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def learn(self):
        for iteration in range(self.args['num_iterations']):
            memory = []

            self.model.eval()
            for selfPlay_iteration in trange(self.args['num_self_play_iterations']):
                memory += self.self_play()

            self.model.train()
            for epoch in trange(self.args['num_epochs']):
                self.train(memory)

            torch.save(self.model.state_dict(), f"model_{iteration}.pt")
            torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}.pt")
