from copy import copy

import chess
class GameManager:
    def __init__(self, player1, player2, board=chess.Board()):
        self.board = board
        self.p1 = player1
        self.p2 = player2

    def reset(self):
        self.board = chess.Board()
        #print(self.board.kings)

    def print_board(self):
        print(self.board)

    def light_playout(self):
        if self.get_turn() == "WHITE":
            return self.play()
        else:
            while not self.board.is_game_over():
                p_2_move = self.p2.get_move(self.board)
                if p_2_move is not None:
                    self.board.push_san(p_2_move)
                p_1_move = self.p1.get_move(self.board)
                if p_1_move is not None:
                    self.board.push_san(p_1_move)
            return self.board.result()

    def play(self):
        while not self.board.is_game_over():
            self.board = self.p1.get_move(copy(self.board))
            p_2_move = self.p2.get_move(self.board)
            if p_2_move is not None:
                self.board.push_san(p_2_move)
            print(str(self.board) + '\n')
        print(str(self.board) + '\n')
        return self.board.result()

    def get_turn(self):
        if self.board.turn:
            return "WHITE"
        else:
            return "BLACK"



