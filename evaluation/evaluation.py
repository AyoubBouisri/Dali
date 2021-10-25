import chess
import time
import math
from random import random

# TODO find a better way
PIECES_ORDER = ['p', 'k', 'q', 'r', 'n', 'b', 'P', 'K', 'Q', 'R', 'N', 'B']

PIECES_WORTH = [1, 3, 3, 5, 9, 0]
MAX_TIME = 1000
MIN_DEPTH = 3


class Evaluator():

    def __init__(self):
        self.transposition_table = []
        self.start_evaluation_time = 0
        self.nbr_moves_searched = 0
        self.max_depth_reached = 0
        self.zobrist_table = self.init_zobrist_table()

    def find_best_move(self, board, isMax):
        hash = self.zobrist_hash(board)
        self.start_evaluation_time = round(time.time() * 1000)
        self.max_depth_reached = 0
        self.nbr_moves_searched = 0
        self.reached_time_limit_mid_search = False

        self.max_depth = MIN_DEPTH

        best_move = self.search_alpha_beta(board, isMax, 0, -math.inf, math.inf)
        while self.current_search_time() < MAX_TIME:
            self.max_depth += 1
            previous_move = best_move
            best_move = self.search_alpha_beta(board, isMax, 0, -math.inf, math.inf)

            if self.reached_time_limit_mid_search:
                self.max_depth_reached -= 1
                best_move = previous_move


        new_hash = self.zobrist_hash_from_previous(hash, best_move[1], board)

        print(f"Eval : {best_move[0]}")
        print(f"Time Searching : {self.current_search_time()}")
        print(f"Depth reached : {self.max_depth_reached}")

        return best_move[1]

    def search_alpha_beta(self, board, isMax, depth, alpha, beta):

        self.max_depth_reached = depth if depth > self.max_depth_reached else self.max_depth_reached
        self.nbr_moves_searched += 1

        if not board.legal_moves or depth >= self.max_depth or self.current_search_time() > MAX_TIME:
            if self.current_search_time() > MAX_TIME:
                self.reached_time_limit_mid_search = True

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
                
    def order_legal_moves(self, board):
        # TODO order moves in a more precise manner
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
        if board.is_checkmate() and board.turn is side:
            eval -= 1000

        # Material
        for i in range(0, len(chess.PIECE_TYPES)):
            eval += PIECES_WORTH[i] * len(board.pieces(chess.PIECE_TYPES[i], side))

        return eval

    def current_search_time(self):
        return time.time() * 1000 - self.start_evaluation_time

    def zobrist_hash_from_previous(self, previous_hash, move, board):
        # TODO 
        to = move.to_square
        fr = move.from_square

        print(board.piece_at(to), board.piece_at(fr))
    
    def init_zobrist_table(self):
        N = 1000
        table = [[0] * 8] * 8
        for i in range(8):
            for j in range(8):
                pieces = []
                for p in range(12):
                    pieces.append(round(random() * N))
                table[i][j] = pieces
        return table

    def zobrist_hash(self, board):
        # TODO probably fix this up with actual algo 
        hash = 0
        board_str = str(board).replace(" ", "").replace("\n", "")
        for i in range(len(board_str)):
            x = i % 8
            y = i // 8 
            if board_str[i] != '.':
                hash = hash ^ self.zobrist_table[x][y][PIECES_ORDER.index(board_str[i])]
        return hash
            

