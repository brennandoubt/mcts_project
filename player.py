import chess
import random


class Player(object):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.color

    def get_move(self, board): pass


class RandomPlayer(Player):
    def __init__(self, color):
        super(RandomPlayer, self).__init__(color)

    def get_move(self, board):
        moves = list(board.legal_moves)
        if len(moves) > 0:
            return board.san(moves[random.randint(0, len(moves) - 1)])
