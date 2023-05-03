import sys
from copy import copy

import player
from player import MCTSNode
import chess
from game_manager import GameManager
def main():
    # Human player usage
    # python3 game_manager.py "WHITE" to play as white
    # python3 game_manager.py "BLACK" to play as black
    if len(sys.argv) == 2:
        board = chess.Board()
        if sys.argv[1] == "WHITE":
            p1 = player.MCTSPlayer('BLACK')
            node = MCTSNode(copy(board))
            player_turn = True
        elif sys.argv[1] == "BLACK":
            p1 = player.AlphaBetaPlayer('WHITE', 3)
            node = MCTSNode(board)
            player_turn = False
        else:
            exit(1)
        # Me playing against the thing, useful for debugging
        while not board.is_game_over():
            print('\n' + str(board))
            if not player_turn:
                player_turn = True
                for _ in range(50):
                    p1.do_rollout(node)
                board = p1.choose(node).board


            else:
                move = input("Enter move: ")
                board.push_san(move)
                node.make_move(move)
                print(node.board)
                player_turn = False

    # Computer Player
    else:
        p1 = player.AlphaBetaPlayer('WHITE', 4)
        p2 = player.AlphaBetaPlayer('BLACK', 4)
        gm = GameManager(p1, p2)
        print(gm.play())


main()