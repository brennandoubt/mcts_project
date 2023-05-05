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

    def heavy_playout(self):
        while not self.board.is_game_over():
            # if self.board.can_claim_fifty_moves():
            #   return "1/2-1/2"
            if self.board.turn:
                p_1_move = self.p1.get_move(self.board)
                if p_1_move is not None:
                    self.board.push_san(p_1_move)
            else:
                p_2_move = self.p2.get_move(self.board)
                if p_2_move is not None:
                    self.board.push_san(p_2_move)
#            print(str(self.board) + '\n')
            # print(str(self.board) + '\n')
        return self.board.result()


    def play(self):
        while not self.board.is_game_over():
            #if self.board.can_claim_fifty_moves():
             #   return "1/2-1/2"
            if self.board.turn:
                p_1_move = self.p1.get_move(self.board)
                if p_1_move is not None:
                    self.board.push_san(p_1_move)
            else:
                p_2_move = self.p2.get_move(self.board)
                if p_2_move is not None:
                    self.board.push_san(p_2_move)
            print(str(self.board) + '\n')
            # print(str(self.board) + '\n')
        return self.board.result()

    def get_turn(self):
        if self.board.turn:
            return "WHITE"
        else:
            return "BLACK"



