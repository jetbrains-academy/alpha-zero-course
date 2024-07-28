In this task, we will simply make sure that the ResNet model can interact with the game interface. 
That is, take an encoded state as input and return an estimate value of the current position 
and a vector of probabilities for the next move (which is random for now).

### Task
Implement model initialization with parameters `num_res_blocks = 4, num_hidden = 64` and apply it to get the value and policy_probs.
