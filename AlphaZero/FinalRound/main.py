import matplotlib.pyplot as plt
import torch

from ResNetEstimator.Model.task import ResNet
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round

from AlphaZero.Training.task import args


if __name__ == "__main__":
    final_round = Round(TicTacToe())
    # player 1
    final_round.play_game(2)
    # player -1
    final_round.play_game(4)
    # player 1
    final_round.play_game(5)
    print("Current game board is:")
    final_round.print_game_layout()

    encoded_state = final_round.instance_of_game.get_board().get_encoded_state()
    print(f"Encoded state = \n{encoded_state}")

    tensor_state = torch.tensor(encoded_state).unsqueeze(0)

    model = ResNet(final_round.instance_of_game, 4, 64)
    model_num = args['num_iterations'] - 1
    model.load_state_dict(torch.load(f'../Training/model_{model_num}.pt'))
    model.eval()

    policy, value = model(tensor_state)
    value = value.item()
    policy = (
        torch.softmax(policy, axis=1)
        .squeeze(0).detach().cpu().numpy()
    )

    print(f"value ={value}")

    plt.bar(range(final_round.instance_of_game.get_board().get_action_size()), policy)
    plt.show()
