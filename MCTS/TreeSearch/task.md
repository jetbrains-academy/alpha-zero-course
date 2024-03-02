## MCTS algorithm
On this step, we will implement MCTS algorithm. 
You don't have to implement everything from scratch — the interface and some methods are already provided.
Take a good look at `Node` and `MCTS` before you start.


### Task
In this task you need to implement all the 4 steps of MCTS search algorithm:
* In selection step you need to go down from the root node until you find a node that can be extended or a termnal node.
In case of terminal node skip extension and simulation steps.
* In expansion step you need to expand the selected node
* In simulation step you need to simulate the random game from the selected node
* In backpropagation step you need to backpropagate the result of the simulation

