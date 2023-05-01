from copy import copy

import chess
import chess.engine
import random
import numpy as np


class Player(object):
    def __init__(self, color):
        self.color = color


    def __str__(self):
        return self.color

    def get_move(self, board): pass


# ----- EVALUATION -----
piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100, 'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 100}

# These are black so flipped
position_values = {
        'P' : np.array([ [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0] ]),

        'N' : np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                       [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                       [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                       [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                       [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                       [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                       [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                       [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0] ]),

        'B' : np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                       [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                       [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                       [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                       [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                       [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                       [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] ]),

        'R' : np.array([[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
                       [ 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                       [ 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]]),

        'Q' : np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                       [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                       [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                       [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                       [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                       [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                       [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

        'K' : np.array([[ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                       [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                       [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                       [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
                       [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]])}
def positionEvaluation(color, position, piece_values=piece_values, position_values=position_values):
    # Once you make the check-mating move then you have two possibilities:

    # 1- You are the one check-mating so the position gets sent into min, and it just returns the -ve evaluation of it.
    # so - (- inf) gives us inf, we want to make that move hence the inf.

    # 2- You are the one getting check-mated so min sends it into max and max returns the +ve evaluation so
    # - inf gives us - inf, we want to avoid it at all costs.

    # The question being why this quirk? Answer: The way I coded this up along with the python chess library.
    # This just makes life easier, instead of trying to go through the code and fix it.
    if position.is_game_over():
        return float('-inf')
    # Position of pieces is not taken into account for their strength
    positionTotalEval = 0
    pieces = position.piece_map()
    for j in pieces:
        file = chess.square_file(j)
        rank = chess.square_rank(j)

        piece_type = str(pieces[j])
        positionArray = position_values[piece_type.upper()]
        if color == 'WHITE':
            if piece_type.isupper():
                flippedPositionArray = np.flip(positionArray, axis=0)
                positionTotalEval += piece_values[piece_type] + flippedPositionArray[rank, file]

            if piece_type.islower():
                positionTotalEval -= piece_values[piece_type]
        if color == 'BLACK':
            if piece_type.isupper():
                positionTotalEval -= piece_values[piece_type]

            if piece_type.islower():
                positionTotalEval += piece_values[piece_type] + position_values[piece_type.upper()][rank, file]

    return positionTotalEval

class RandomPlayer(Player):
    def __init__(self, color):
        super(RandomPlayer, self).__init__(color)

    def get_move(self, board):
        moves = list(board.legal_moves)
        if len(moves) > 0:
            return board.san(moves[random.randint(0, len(moves) - 1)])


class DeterministicPlayer(Player):
    def __init__(self, color):
        super(DeterministicPlayer, self).__init__(color)

    def get_move(self, board):
        moves = list(board.legal_moves)
        if len(moves) > 0:
            print(moves[0])
            return board.san(moves[1])


class MiniMaxPlayer(Player):
    def __init__(self, color, depth):
        super(MiniMaxPlayer, self).__init__(color)
        self.depth = depth
        self.multiply = 1
        if self.color == 'WHITE':
            self.other_color = 'BLACK'
            #self.multiply = -1
        else:
            self.other_color = 'WHITE'


    def get_move(self, board):
        v = float('-inf')
        finalMove = None
        legalMoves = list(board.legal_moves)
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._minValue(newBoard, 1)
            print(str(check) + ", " + board.san(move))
            if v < check:
                v = check
                print(v)
                finalMove = board.san(move)
        return finalMove
    def _maxValue(self, board, d):
        legalMoves = list(board.legal_moves)
        if d >= self.depth or board.is_game_over():
            return positionEvaluation(self.color, board)
        v = float('-inf')
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._minValue(newBoard, d + 1)
            if v < check:
                v = check
        return v
    def _minValue(self, board, d):
        legalMoves = list(board.legal_moves)
        if d >= self.depth or board.is_game_over():
            return -positionEvaluation(self.other_color, board)
        v = float('inf')
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._maxValue(newBoard, d + 1)
            if v > check:
                v = check
        return v


