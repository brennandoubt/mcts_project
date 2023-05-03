import math
from copy import copy
import chess
import chess.engine
import random
import numpy as np


class Player(object):
    def __init__(self, color):
        self.color = color
        if self.color == 'WHITE':
            self.other_color = 'BLACK'
        else:
            self.other_color = 'WHITE'

    def __str__(self):
        return self.color

    def get_move(self, board):
        pass


# ----- EVALUATION -----
piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 100, 'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90,
                'k': 100}

# These are black so flipped
position_values = {
    'P': np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                   [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                   [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                   [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                   [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                   [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]),

    'N': np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                   [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                   [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                   [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                   [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                   [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                   [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                   [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]),

    'B': np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                   [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                   [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                   [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                   [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                   [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                   [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]),

    'R': np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                   [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                   [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]),

    'Q': np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                   [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                   [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                   [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                   [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                   [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

    'K': np.array([[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                   [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                   [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                   [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                   [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]])}


def positionEvaluation(color, position, piece_values=piece_values, position_values=position_values):
    # Once you make the check-mating move then you have two possibilities:

    # 1- You are the one check-mating so the position gets sent into min, and it just returns the -9999999
    # evaluation of it. So - (- 9999999) gives us 9999999, we want to make that move, it wins the game hence the
    # 9999999.

    # 2- You are the one getting check-mated so min sends it into max and max returns the +ve evaluation so
    # -9999999 gives us - inf, we want to avoid it at all costs.

    # The question being why this quirk? Answer: The way I coded this up along with the python chess library.
    # This just makes life easier, instead of trying to go through the code and fix it.
    if position.is_checkmate():
        return -9999999
    if position.is_stalemate():
        return 0
    # Position of opponent's pieces is not taken into account for their strength
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
                positionTotalEval += piece_values[piece_type] + positionArray[rank, file]

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

    def get_move(self, board):
        v = float('-inf')
        finalMove = None
        legalMoves = list(board.legal_moves)
        if len(legalMoves) == 1:
            return board.san(legalMoves[0])
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._minValue(newBoard, 1)
            if v < check:
                v = check
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


class AlphaBetaPlayer(Player):
    def __init__(self, color, depth):
        super(AlphaBetaPlayer, self).__init__(color)
        self.depth = depth

    def get_move(self, board):
        v, alpha, beta, finalMove = float('-inf'), float('-inf'), float('inf'), None
        legalMoves = list(board.legal_moves)
        if len(legalMoves) == 1:
            return board.san(legalMoves[0])
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._minValue(newBoard, 1, alpha, beta)
            # print(str(check) + ", " + board.san(move))
            if v < check:
                v = check
                finalMove = board.san(move)
            if alpha < v:
                alpha = v
        return finalMove

    def _maxValue(self, board, d, a, b):
        legalMoves = list(board.legal_moves)
        if d >= self.depth or board.is_game_over():
            return positionEvaluation(self.color, board)
        v = float('-inf')
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._minValue(newBoard, d + 1, a, b)
            if v < check:
                v = check
            if v >= b:
                return v
            if a < v:
                a = v
        return v

    def _minValue(self, board, d, a, b):
        if d >= self.depth or board.is_game_over():
            return -positionEvaluation(self.other_color, board)
        legalMoves = list(board.legal_moves)
        v = float('inf')
        for move in legalMoves:
            newBoard = copy(board)
            newBoard.push_san(board.san(move))
            check = self._maxValue(newBoard, d + 1, a, b)
            if v > check:
                v = check

            if v <= a:
                return v
            if b > v:
                b = v
        return v


class MCTSNode:
    def __init__(self, state=chess.Board(), action=None, children=None, parent=None, x=0, n=0, n_i=1):
        if children is None:
            children = []
        self.state = state
        self.action = action
        self.children = children
        self.parent = parent

        # for UCB calculation
        self.x = x  # Average payout ---> Times the color of the node won / n_i
        self.n = n  # How many times the parent node has been simulated
        self.n_i = n_i  # How many times has the node been simulated

    def ucb(self):
        return self.x + ((math.sqrt(2 * math.log(self.n, 2))) / self.n_i)

    def __str__(self):
        string = "-----PRINTING MCTS NODE-----\n BOARD: \n" + str(self.state) + '\n' + " PARENT: \n" + "     " + str(
            self.parent)
        if self.action is not None:
            string += '\n' + "ACTION: " + self.parent.state.san(self.action)
        return string


class MCTSPlayer(Player):
    def __init__(self, color, rounds, start_board):
        super(MCTSPlayer, self).__init__(color)
        self.rounds = rounds
        self.root = MCTSNode(start_board)

    def selection(self, node):
        while len(node.children) > 0:
            candidate = node
            max_ucb = float('-inf')
            for child in node.children:
                if child.ucb() > max_ucb:
                    max_ucb = child.ucb()
                    candidate = child
            node = candidate
        return node

    def expansion(self, node):
        actions = list(node.state.legal_moves)
        for move in actions:
            newBoard = copy(node.state)
            newBoard.push_san(newBoard.san(move))
            child = MCTSNode(newBoard, move, [], node)
            node.children.append(child)
        if len(node.children) > 0:
            return node.children[random.randint(0, len(node.children) - 1)]
        else:
            node = self.selection()

    def simulation(self, node):
        board = node.state
        while not board.is_game_over():
            legal_moves = list(board.legal_moves)
            if len(legal_moves) > 0:
                board.push_san(board.san(legal_moves[random.randint(0, len(legal_moves) - 1)]))
        if (board.result() == "1-0" and self.color == 'WHITE') or (board.result() == "0-1" and self.color == 'BLACK'):
            return 1

        if (board.result() == "1-0" and self.color == 'BLACK') or (board.result() == "0-1" and self.color == 'WHITE'):
            return 0

        else:
            return 0.5

    def update(self, node, val):
        while node is not None:
            node.x += val
            print("X: ", str(node.x))
            node.n_i += 1
            for child in node.children:
                child.n += 1
            node = node.parent

    def get_move(self, board):
        self.root = MCTSNode(board)
        for i in range(self.rounds):
            print("N before " + str(self.root.n_i))
            node = self.selection(self.root)
            child = self.expansion(node)
            simulation = self.simulation(child)  # 1 if we won, -1 won if we lost, 0 if we drew
            self.update(child, simulation)

        max_payout = float('-inf')
        action = None
        for child in self.root.children:
            payout = child.x / child.n_i
            if payout > max_payout:
                max_payout = payout
                action = board.san(child.action)
        print(action)
        return action

