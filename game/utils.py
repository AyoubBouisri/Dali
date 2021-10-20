import chess
import pygame


def get_move(from_sq, to_sq):
    if from_sq == to_sq:
        return None

    def to_string(i, j):
        a = 97 # ASCII for 'a'
        return chr(a + i) + str( 8 - j)
    uci = to_string(*from_sq) + to_string(*to_sq)
    return chess.Move.from_uci(uci)
        

def get_pieces_png():
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

    return piece_dict, image

