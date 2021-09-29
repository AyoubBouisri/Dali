import pygame
import chess

class Game():
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.screen = pygame.display.set_mode([self.w, self.h])
        self.square_w = w // 8
        self.pieces_img = self.get_pieces_png()
        self.board = chess.Board()

    def draw(self):
        self.draw_background()
        self.draw_pieces()
        pygame.display.update()


    def draw_pieces(self):
        board_str = str(self.board).replace(" ", "").replace("\n", "")
        for i in range(len(board_str)):
            x = i % 8 * self.square_w 
            y = i // 8 * self.square_w 
            c = board_str[i]

            if c in self.pieces_img:
                self.screen.blit(self.pieces_img[c], (x,y))
                



    def draw_background(self):
        for i in range(0,8):
            for j in range(0,8):
                color = (245, 223, 164) if (i + j) % 2 == 0 else (219, 162, 7)
                pygame.draw.rect(self.screen, color, pygame.Rect(i * self.square_w, j * self.square_w, self.square_w, self.square_w))

    def update(self):
        pass

    def get_pieces_png(self):
        piece_order = ['k', 'q', 'r', 'n', 'b', 'p']
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
                piece_img = pygame.Surface(rect.size).convert_alpha() 
                piece_img.blit(image,(0,0), rect)
                piece_dict[piece] = piece_img
                
            piece_order = [piece.upper() for piece in piece_order]

        return piece_dict



        