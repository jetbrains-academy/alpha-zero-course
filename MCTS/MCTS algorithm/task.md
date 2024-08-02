In this module, you will create a basic **Monte Carlo Tree Search (MCTS)** algorith.
The main idea of the MCTS is to randomly simulate possible outcomes of a
decision space, like moves in a game, without exploring every option. 
This gives a good estimate of the best moves, so the algorithm can focus 
on the more promising parts of the decision tree. If you're not familiar with MCTS,
you may want to read more before proceeding to the next steps. Our team suggests checking out
<a href="https://youtu.be/wuSQpLinRB4?t=343&si=IU8DwHXrLPsiEAXv" target="_blank">this video</a>

**Decision tree** represents the possible moves in a game from the different states.
Each **node** in the decision tree corresponds to a game state.
The root node represents the current state of the game from 
which the search begins.
Each child node is a potential future state that results from a specific 
move made from the parent state.

Each **edge** represents a move that transitions from one state to another.

During the algorithm, we will update the tree based on the sampled strategy, so we need to know the possible
child states for each node.


MCTS consists of four main steps that work in a repetitive cycle. These steps are Selection, Expansion, Simulation, and Backpropagation.

1. **Selection**: During this step, we use a tree policy to find a path that connects the root node with the most promising 
leaf node. A leaf node is a node that contains unexplored child node(s). 
If node is fully-expanded, algorithm chooses child nodes to explore using a policy that balances finding new nodes with using known good ones.
We will use UCB formula to that:
$$UCB(node) = \text{mean_node_value} + c*\sqrt{\frac{\log N}{n}},$$
where $n$ — number of visits of the node, $N$ — number of visits of the parent node.
The process continues until a leaf node representing an unexplored position is reached. 
If the algorithm reached a terminal node, selection stops and goes straight to backpropagation.

2. **Expansion**: Once the process reaches a node that has not been fully expanded 
(i.e., not all possible moves from that node have been explored), one of the possible child nodes is added to the tree.

3. **Simulation**: A simulation is started from this new point by making random moves until the game ends (win, loss, or draw).

4. **Backpropagation**: The simulation result is used to update information in the nodes on the path from the root to the expanded node. 
This includes updating the win/loss statistics of each node, which provides feedback on the node's potential based on the simulation outcome.

During the decision-making process, the algorithm goes through a cycle of selection, expansion, simulation, and backpropagation. 
This cycle is repeated multiple times. Each time, new nodes are added to the tree to represent game states, and the edges represent moves. 
The nodes store statistics that show the success rate of the explored game paths.
When it's time to make a move, the algorithm selects the most promising next step. 
This is usually the move that leads to the child node with the highest win rate or the most simulations, 
depending on the criteria used by the implementation to determine the "best" move.

