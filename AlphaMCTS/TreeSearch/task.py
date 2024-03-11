import numpy as np
import torch

from AlphaMCTS.TreeNode.task import Node


class AlphaMCTS:
    def __init__(self, game, args, model):
        self.game = game
        self.args = args
        self.model = model

    @torch.no_grad()
    def search(self, state):
        root = Node(self.game, self.args, state)

        for search in range(self.args['num_searches']):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            if node.action_taken is None:
                value = 0
            else:
                value = self.game.get_game_ended(node.state, node.get_player())
            value = self.game.get_opponent_value(value)

            if not value:
                policy, value = self.model(
                    torch.tensor(self.game.get_encoded_state(node.state)).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.game.get_valid_moves(node.state)
                policy *= valid_moves
                policy /= np.sum(policy)

                value = value.item()
                node.expand(policy)

            # backpropagation
            node.backpropagate(value)

        action_probs = np.zeros(self.game.get_action_size())
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
