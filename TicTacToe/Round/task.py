from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe


class Round:
    def __init__(self, instance_of_game):
        self.instance_of_game = instance_of_game
        self.player = 1

    def print_game_layout(self):
        print(self.instance_of_game.get_board())
        valid_moves = self.instance_of_game.get_valid_moves()
        print("valid_moves",
              [i for i in range(self.instance_of_game.get_board().get_action_size())
               if valid_moves[i] == 1])
        print(f"{self.player}:", end="")

    def play_game(self, action):
        valid_moves = self.instance_of_game.get_valid_moves()
        if valid_moves[action] == 0:
            print("action not valid")
            return True

        self.instance_of_game._board = self.instance_of_game.get_next_state(
            self.instance_of_game.get_board(), self.player, action
        )

        value = self.instance_of_game.get_game_ended(
            self.instance_of_game.get_board(), self.player
        )

        if value:
            print(self.instance_of_game.get_board())
            if value == 1:
                print(self.player, "won")
            elif value == -1:
                print(-self.player, "won")
            else:
                print("draw")
            return False

        self.player = self.instance_of_game.get_opponent(self.player)
        return True


if __name__ == '__main__':
    first_round = Round(TicTacToe(Board()))
    is_playing = True
    while is_playing:
        first_round.print_game_layout()
        choose = int(input())
        is_playing = first_round.play_game(choose)
