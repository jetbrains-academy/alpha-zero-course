After we've taken care of storing the board, let's implement the interface of the Dots and Boxes game itself. 
We will inherit the `TicTacToe` class and change only two methods according to the logic of the game. 

In the `DotsAndBoxes` game, `action` means number of line which player has chosen for his move. Numbering is through, by rows, starts from zero. Remember that firstly we enumerate horizontal lines, then vertical.
That is, for action 5 on the 3x3 board you will select the horizontal line with index `(1, 2)`. 

### Task
In this task you need to implement some missing functionality of `DotsAndBoxes` class:
1. In `get_next_state` function calculate indexes by the `action` number (look description above)
2. In `change_perspective` function invert the board. For `player` board should stay the same, but for `-player` 1 and -1 should be flipped
