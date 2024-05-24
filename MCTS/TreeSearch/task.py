import numpy as np

from MCTS.TreeNode.task import Node


class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state):
        root = Node(self.game, self.args, state)

        for search in range(self.args['num_searches']):
            node = root
            # selection
            while node.is_fully_expanded():
                node = node.select()

            if node.action_taken is None:
                value = 0
            else:
                value = self.game.get_game_ended(node.state, node.get_player())

            value = self.game.get_opponent_value(value)

            if not value: # if not a terminal node
                # expansion
                node = node.expand()
                # simulation
                value = node.simulate()
            # backpropagation
            node.backpropagate(value)

        # return actions probabilities
        action_probs = np.zeros(self.game.get_board().get_action_size())
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
