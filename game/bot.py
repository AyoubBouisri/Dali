import chess
from .utils import board_eval
from random import randrange



class Dali():
    def __init__(self):
        pass

    def eval_move(self, board, move):
        board.push(move)
        eval = board_eval(board)
        board.pop()
        return eval

    def play(self, board):
        legal_moves = list(board.legal_moves)
        best_move = (legal_moves[randrange(len(legal_moves))], 0)
        
        for i in range(0, len(legal_moves)):
            move = legal_moves[i]
            eval = self.eval_move(board, move)
            if eval < best_move[1]:
                best_move = (move, eval)
                
        board.push(best_move[0])
