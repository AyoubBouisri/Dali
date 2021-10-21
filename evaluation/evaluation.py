import chess
from datetime import datetime


PIECES_WORTH = [1, 3, 3, 5, 9, 0]
TIME_LIMIT = 5000 # ms


class Evaluator():

    def __init__(self):
        self.transposition_table = []
        self.start_evaluation_time = 0
        self.nbr_moves_searched = 0

    def find_best_move(self, board, isMax):
        self.start_evaluation_time = datetime.now()
        best_move = self.search(board, isMax, 0)

        print(self.get_search_time())
        return best_move[1]

    def search(self, board, isMax, depth):

        current_time = self.get_search_time()

        if not board.legal_moves or current_time > TIME_LIMIT:
            return eval_position(board), None
        
        moves = []
        for move in board.legal_moves:
            board.push(move)
            best_move, nbr_moves= find_best_move(board, not isMax, depth)
            moves.append(best_move[0], move)
            board.pop()

        return get_edge_moves(moves, isMax)


    def get_edge_moves(moves, isMax):
        if isMax:
            return max(moves, key=lambda t: t[0])
        else:
            return min(moves, key=lambda t: t[0])


    def order_moves():
        pass


    def eval_position(board):
        white_eval = side_eval(chess.WHITE, board)
        black_eval = side_eval(chess.BLACK, board)
        return white_eval - black_eval


    def side_eval(side, board):
        eval = 0

        # Check if the side lost the game
        if board.is_checkmate and board.turn is side:
            eval -= 1000

        # Material
        for i in range(0, len(chess.PIECE_TYPES)):
            eval += PIECES_WORTH[i] * len(board.pieces(chess.PIECE_TYPES[i], side))

        return eval

    def get_search_time(self):
        return datetime.now() - self.start_evaluation_time

    def zobrist_hash(board):
        pass

    def get_position(board):
        pass


