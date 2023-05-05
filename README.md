# mcts_project
Project demonstrating Monte Carlo Tree Search and comparing with Minimax and Alpha-Beta Pruning using chess games.

## Overview
In this project, we are demonstrating the Monte Carlo Tree Search algorithm by comparing it against the performance of two other game search algorithms: Minimax and Alpha-Beta pruning. In order to properly demonstrate this, we will be using a control agent that will play chess against another agent that uses each of these algorithms. We will then compare the performance of the Minimax agent, Alpha-Beta pruning agent, and the Monte Carlo Tree Search agent against the control agent by analyzing the chess games each of them played and seeing how well they performed against the control agent.


## How to Run:

1- Install chess.py ---> pip3 install chess


2- Run main file to play Alpha Beta against Minimax and MCTS against Alpha Beta


3- Arguments of players:

Minimax and Alpha-Beta (color: which color are they, depth)

MCTS(color: which color is it, number of rounds: how many rounds to run the 4 step process, starting board)
