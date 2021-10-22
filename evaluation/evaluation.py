import chess
import time
import math

PIECES_WORTH = [1, 3, 3, 5, 9, 0]
TIME_LIMIT = 10000 # ms
MAX_DEPTH = 3


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

        #best_move = self.search_min_max(board, isMax, 0)
        best_move = self.search_alpha_beta(board, isMax, 0, -math.inf, math.inf)

        print(f"Depth Reached : {self.max_depth_reached}")
        print(f"Time Searching : {self.get_search_time()}")
        print(f"Moves Searched : {self.nbr_moves_searched}")

        return best_move[1]

    def search_alpha_beta(self, board, isMax, depth, alpha, beta):

        self.max_depth_reached = depth if depth > self.max_depth_reached else self.max_depth_reached
        self.nbr_moves_searched += 1

        if not board.legal_moves or depth >= MAX_DEPTH:
            return self.eval_position(board), None
        
        if isMax:
            max_value = (-math.inf, None)
            for move in self.order_legal_moves(board):
                board.push(move)
                best_move = self.search_alpha_beta(board, False, depth + 1, alpha, beta)
                board.pop()

                max_value = max([max_value, (best_move[0], move)], key=lambda t:t[0])
                alpha = max(alpha, best_move[0]) 
                if beta <= alpha:
                    break
            return max_value
        else:
            min_value = (math.inf, None)
            for move in self.order_legal_moves(board):
                board.push(move)
                best_move = self.search_alpha_beta(board, True, depth + 1, alpha, beta)
                board.pop()

                min_value = min([min_value, (best_move[0], move)], key=lambda t: t[0])
                beta = min(best_move[0], beta)
                if beta <= alpha:
                    break
            return min_value
                
    def search_min_max(self, board, isMax, depth):
        self.max_depth_reached = depth if depth > self.max_depth_reached else self.max_depth_reached
        self.nbr_moves_searched += 1

        if not board.legal_moves or depth >= MAX_DEPTH:
            return self.eval_position(board), None
        
        moves = []
        for move in board.legal_moves:
            board.push(move)
            best_move = self.search_min_max(board, not isMax, depth + 1)
            moves.append((best_move[0], move))
            board.pop()

        return self.get_edge_moves(moves, isMax)

    def get_edge_moves(self, moves, isMax):
        if isMax:
            return max(moves, key=lambda t: t[0])
        else:
            return min(moves, key=lambda t: t[0])

    def order_legal_moves(self, board):
        checks = []
        piece_attacks = []
        others = []
        
        moves = board.legal_moves
        for move in moves:
            board.push(move)
            if board.is_check():
                checks.append(move)
            else:
                is_attacking = False
                squares_attacked = board.attacks(move.to_square)
                for square in squares_attacked:
                    piece = board.piece_at(square) 
                    if piece and piece.color == board.turn:
                        piece_attacks.append(move)
                        is_attacking = True
                        break;

                if not is_attacking:
                    others.append(move)
            board.pop()

        return checks + piece_attacks + others

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


