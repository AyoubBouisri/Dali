import chess
from random import randrange


PIECES_WORTH= [1, 3, 3, 5, 9, 0]
MAX_DEPTH = 2


class Dali():

    def play(self, board, last_move):
        best_move = self.find_best_move(board)
        board.push(best_move[1])

    # Dali is trying to Minimize
    def find_best_move(self, board, isMax=False, depth=0):
        if not board.legal_moves:
            return self.eval(board), board.peek()

        if depth == MAX_DEPTH:
            evals = [(self.eval_move(board, move, play=True), move) for move in board.legal_moves] 
            return self.get_edge_move(evals, isMax)

        evals = []
        for move in board.legal_moves:
            board.push(move)
            best_move = self.find_best_move(board, isMax=(not isMax), depth=depth+1)
            if best_move:
                evals.append((best_move[0], move))
            board.pop()

        return self.get_edge_move(evals, isMax)
    
    def get_edge_move(self, moves, isMax):
        if moves:
            if isMax:
                return max(moves, key=lambda t: t[0])
            else:
                return min(moves, key=lambda t: t[0])
        return None



