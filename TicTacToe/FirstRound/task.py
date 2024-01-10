from TicTacToe.GameImplementation.Game import TicTacToe


class FirstRound:
    def __init__(self):
        self.tictactoe = TicTacToe()
        self.player = 1
        self.board = self.tictactoe.get_init_board()

    def print_game_layout(self):
        print(self.board)
        valid_moves = self.tictactoe.get_valid_moves(self.board)
        print("valid_moves", [i for i in range(self.tictactoe.get_action_size()) if valid_moves[i] == 1])
        print(f"{self.player}:")

    def play_game(self, action):
        valid_moves = self.tictactoe.get_valid_moves(self.board)
        if valid_moves[action] == 0:
            print("action not valid")
            return True

        self.board = self.tictactoe.get_next_state(self.board, self.player, action)

        value = self.tictactoe.get_game_ended(self.board, self.player)

        if value:
            print(self.board)
            if value == 1:
                print(self.player, "won")
            elif value == -1:
                print(-self.player, "won")
            else:
                print("draw")
            return False

        self.player = self.tictactoe.get_opponent(self.player)
        return True


if __name__ == '__main__':
    first_round = FirstRound()
    is_playing = True
    while is_playing:
        first_round.print_game_layout()
        choose = int(input())
        is_playing = first_round.play_game(choose)
