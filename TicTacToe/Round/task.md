### Playing the game
Yay! It's finally time to play!

In this step, we'll implement an interactive interface for Tic-tac-toe. Try playing with someone together or with yourself (don't give in!).

### Task
Complete the parts of the code following the rules:
- List of valid moves should be printed in the format: `valid_moves [<posible_actions>]`. For example, before first action, it will consist of all possible actions `valid_moves [0, 1, 2, 3, 4, 5, 6, 7, 8]`
- `play_game` function should return `True` if game is not ended
- If `play_game` function receive `action` which not valid, print `action not valid` and exit the function
- If `player` is won, print `1 won`
- If `-player` is won, print `-1 won`
- Print `draw` if game ends with draw

Example of possible game log (to better ensure what the output should be):
```
---
---
---

valid_moves [0, 1, 2, 3, 4, 5, 6, 7, 8]
1:0
X--
---
---

valid_moves [1, 2, 3, 4, 5, 6, 7, 8]
-1:8
X--
---
--O

valid_moves [1, 2, 3, 4, 5, 6, 7]
1:3
X--
X--
--O

valid_moves [1, 2, 4, 5, 6, 7]
-1:5
X--
X-O
--O

valid_moves [1, 2, 4, 6, 7]
1:6
X--
X-O
X-O

1 won
```