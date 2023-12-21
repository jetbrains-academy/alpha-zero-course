import matplotlib.pyplot as plt
import torch

from TicTacToe.GameImplementation.Game import TicTacToe
from ResNetEstimator.Model.task import ResNet

tictactoe = TicTacToe()

state = tictactoe.get_init_board()
state = tictactoe.get_next_state(state, 1,2)
state = tictactoe.get_next_state(state, -1, 7)

encoded_state = tictactoe.get_encoded_state(state)

tensor_state = torch.tensor(encoded_state).unsqueeze(0)

model = ResNet(tictactoe, 4, 64)
model.eval()

policy, value = model(tensor_state)
value = value.item()
policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()

print(value)

print(state)
print(tensor_state)

plt.bar(range(tictactoe.get_action_size()), policy)
plt.show()
