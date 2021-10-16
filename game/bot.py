import chess
from .utils import board_eval
from random import randrange



class Dali():
    def __init__(self):
        pass

    def eval(board):
        pass 


    def play(self, board):
        legal_moves = list(board.legal_moves)
        best_move = (legal_moves[0], 0)
        
        for i in range(0, len(legal_moves)):
            move = legal_moves[i]
            board.push(move)
            eval = board_eval(board)
            if eval < best_move[1]:
                best_move = (move, eval)
            board.pop()
                
        board.push(best_move[0])
