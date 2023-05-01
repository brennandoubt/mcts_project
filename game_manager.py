import chess
from copy import deepcopy
import player


class GameManager:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.p1 = player1
        self.p2 = player2

    def reset(self):
        self.board = chess.Board()
        #print(self.board.kings)

    def print_board(self):
        print(self.board)

    def play(self):
        while not self.board.is_game_over():
            p_1_move = self.p1.get_move(self.board)
            if p_1_move is not None:
                self.board.push_san(p_1_move)
            p_2_move = self.p2.get_move(self.board)
            if p_2_move is not None:
                print("hi")
                self.board.push_san(p_2_move)
            print(str(self.board) + '\n')
        return self.board.result()

    def get_turn(self):
        if self.board.turn:
            return "WHITE"
        else:
            return "BLACK"


def main():
    p1 = player.MiniMaxPlayer('WHITE', 2)
    #player_turn = False
    p2 = player.RandomPlayer('BLACK')
    board = chess.Board()
    '''
    # Me playing against the thing, useful for debugging
    while not board.is_game_over():
        print('\n' + str(board))
        if not player_turn:
            board.push_san(p1.get_move(board))
            player_turn = True
        else:
            move = input("Enter move: ")
            board.push_san(move)
            player_turn = False
    '''
    gm = GameManager(p1, p2)
    print(gm.play())


main()
