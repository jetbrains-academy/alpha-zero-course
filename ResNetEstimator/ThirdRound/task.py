import matplotlib.pyplot as plt
import torch

from TicTacToe.Round.task import Round
from ResNetEstimator.Model.task import ResNet


def init_and_apply_nn(round):
    encoded_state = round.instance_of_game.get_encoded_state(round.board)
    tensor_state = torch.tensor(encoded_state).unsqueeze(0)
    model = ResNet(round.instance_of_game, 4, 64)
    policy, value = model(tensor_state)

    value_item = value.item()
    policy_probs = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
    return value_item, policy_probs


if __name__ == '__main__':
    third_round = Round()
    # player 1
    third_round.play_game(2)
    # player -1
    third_round.play_game(7)
    print("Current game board is:")
    third_round.print_game_layout()

    encoded_state = third_round.instance_of_game.get_encoded_state(third_round.board)
    print(f"Encoded state = \n{encoded_state}")

    value, policy_probs = init_and_apply_nn(third_round)
    print(f"Value = {value}, policy_probs = {policy_probs}")

    plt.bar(range(third_round.instance_of_game.get_action_size()), policy_probs)
    plt.show()
