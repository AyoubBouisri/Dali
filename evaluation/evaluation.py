import chess
import time

PIECES_WORTH = [1, 3, 3, 5, 9, 0]
TIME_LIMIT = 2000 # ms
MAX_DEPTH = 5


class Evaluator():

    def __init__(self):
        self.transposition_table = []
        self.start_evaluation_time = 0
        self.nbr_moves_searched = 0
        self.max_depth_reached = 0

    def find_best_move(self, board, isMax):
        self.start_evaluation_time = round(time.time() * 1000)
        self.max_depth_reached = 0
        self.nbr_moves_searched = 0

        best_move = self.search(board, isMax, 0)

        print(f"Depth Reached : {self.max_depth_reached}")
        print(f"Time Searching : {self.get_search_time()}")
        print(f"Moves Searched : {self.nbr_moves_searched}")

        return best_move[1]

    def search(self, board, alpha, beta, isMax, depth):

        self.max_depth_reached = depth if depth > self.max_depth_reached else self.max_depth_reached
        self.nbr_moves_searched += 1

        if not board.legal_moves or self.get_search_time() > TIME_LIMIT or depth >= MAX_DEPTH:
            return self.eval_position(board), None
        
        moves = []
        for move in board.legal_moves:
            board.push(move)
            best_move = self.search(board, not isMax, depth + 1)
            moves.append((best_move[0], move))
            board.pop()

        return self.get_edge_moves(moves, isMax)

    def get_edge_moves(self, moves, isMax):
        if isMax:
            return max(moves, key=lambda t: t[0])
        else:
            return min(moves, key=lambda t: t[0])

    def order_moves(self):
        pass

    def eval_position(self, board):
        white_eval = self.side_eval(chess.WHITE, board)
        black_eval = self.side_eval(chess.BLACK, board)
        return white_eval - black_eval

    def side_eval(self, side, board):
        eval = 0

        # Check if the side lost the game
        if board.is_checkmate and board.turn is side:
            eval -= 1000

        # Material
        for i in range(0, len(chess.PIECE_TYPES)):
            eval += PIECES_WORTH[i] * len(board.pieces(chess.PIECE_TYPES[i], side))

        return eval

    def get_search_time(self):
        return time.time() * 1000 - self.start_evaluation_time

    def zobrist_hash(self, board):
        pass

    def get_position(self, board):
        pass


