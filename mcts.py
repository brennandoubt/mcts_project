import chess
import chess.engine
import math
import random


class MctsNode:
    def __init__(self):
        self.state = chess.Board()
        self.action = ''
        self.children = set()
        self.parent = None

        # for UCB calculation
        self.X = 0
        self.n = 0
        self.n_i = 0


def ucb(curr_node):
    return curr_node.X + math.sqrt(2 * math.log(curr_node.n, 2) / curr_node.ni)


# Random player

def random_player():
    board = chess.Board()
    print(chess.WHITE)
    #while ((not board.is_game_over())):
    for i in range(2):
        moves = list(board.legal_moves)
        if(len(moves) != 0):
            board.push_san(board.san(moves[random.randint(0, len(moves) - 1)]))
        #print(board.turn)

random_player()