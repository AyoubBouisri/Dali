import pygame
import chess

class Game():
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.screen = pygame.display.set_mode([self.w, self.h])
        self.square_w = w // 8
        self.pieces_img = self.get_pieces_png()
        self.board = chess.Board()
        self.board_array = self.update_board()

        self.is_dragging = False
        self.current_piece = None # Piece that the player is dragging

    def draw(self):
        self.draw_background()
        self.draw_pieces()
        pygame.display.update()

    def mouse_pressed(self, mouse_pos):
        i, j = mouse_pos[0] // self.square_w, mouse_pos[1] // self.square_w
        if self.board_array[i][j] != '.':
            self.current_piece = (i,j)
            self.mouse_pos = mouse_pos

    def mouse_released(self, mouse_pos):
        if self.current_piece:
            i, j = mouse_pos[0] // self.square_w, mouse_pos[1] // self.square_w
            move = self.get_move(self.current_piece, (i,j))

            if move in self.board.legal_moves:
                self.board.push(move)
                self.board_array = self.update_board()

            self.current_piece = None
        
    def mouse_moved(self, mouse_pos):
        if self.current_piece:
            self.mouse_pos = mouse_pos

    def update_board(self):
        board_array = [ [0] * 8 for _ in range(8)]
        board_str = str(self.board).replace(" ", "").replace("\n", "")
        for i in range(len(board_str)):
            x = i % 8
            y = i // 8 
            board_array[x][y] = board_str[i]
        return board_array

    def draw_pieces(self):
        for i in range(len(self.board_array)):
            for j in range(len(self.board_array[i])):
                x = i * self.square_w 
                y = j * self.square_w 
                c = self.board_array[i][j]
                if c in self.pieces_img:
                    img_size = self.pieces_img[c].size
                    x = x + self.square_w / 2 - img_size[0] / 2
                    y = y + self.square_w / 2 - img_size[0] / 2
                    if self.current_piece:
                        current_i, current_j = self.current_piece[0], self.current_piece[1]
                        if current_i == i and current_j == j:
                            x = self.mouse_pos[0] - img_size[0] / 2
                            y = self.mouse_pos[1] - img_size[0] / 2
                    self.screen.blit(self.pieces_sprites, pygame.Rect(x, y,self.square_w, self.square_w), area=self.pieces_img[c])

    def draw_background(self):
        for i in range(0,8):
            for j in range(0,8):
                color = (251, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, pygame.Rect(i * self.square_w, j * self.square_w, self.square_w, self.square_w))

    def update(self):
        pass

    def get_pieces_png(self):
        piece_order = ['q', 'k', 'r', 'n', 'b', 'p']
        image = pygame.image.load('resources/pieces.png').convert_alpha()
 
        img_w, img_h = image.get_size()
        piece_w = img_w / len(piece_order)
        piece_h = img_h / 2

        piece_dict = {}
        # set up the black pieces 
        for j in range(0, 2): 
            for i in range(len(piece_order)):
                piece = piece_order[i]
                rect = pygame.Rect(i * piece_w, j * piece_h, piece_w, piece_h)
                piece_dict[piece] = rect
            piece_order = [piece.upper() for piece in piece_order]

        self.pieces_sprites = image

        return piece_dict

    def get_move(self, from_sq, to_sq):
        if from_sq == to_sq:
            return None

        def to_string(i, j):
            a = 97 # ASCII for 'a'
            return chr(a + i) + str( 8 - j)
        uci = to_string(*from_sq) + to_string(*to_sq)
        print(uci)
        return chess.Move.from_uci(uci)
            
        




        