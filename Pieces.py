import pygame
from Functions import to_idx


fig_dict = {0: "White Blank", 1: "Black Blank", 2: "White Pawn", 3: "White Bishop",
            4: "White Knight", 5: "White Rook", 6: "White Queen", 7: "White King",
            8: "Black Pawn", 9: "Black Bishop", 10: "Black Knight", 11: "Black Rook",
            12: "Black Queen", 13: "Black King"}

letter_dict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}


class Piece(pygame.sprite.Sprite):
    def __init__(self, colour, letter, number, cash_pos=None, square=None):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.letter = letter
        self.number = number
        self.cash_pos = cash_pos
        self.draw = True
        self.name = 'Piece'
        self.is_king = False
        self.is_pawn = False
        self.square = square

    def put_on_board(self, board):
        i = to_idx(self.letter, self.number)
        self.square = board.position[i[1]][i[0]]

    def move_on_board(self, square):
        self.square = square

    def change_place(self, letter, number):
        self.letter = letter
        self.number = number
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)

    def move_freely(self, x, y):
        self.rect.center = (x, y)

    def delete_piece(self):
        self.draw = False

    def can_draw(self):
        return self.draw

    def get_colour(self):
        return self.colour

    def check_king(self):
        return self.is_king


class Pawn(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White Pawn.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black Pawn.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)
        self.is_pawn = True

    def can_move(self, square, _, __):
        s_coord = square.give_letter_and_number()
        if self.colour == 0 and s_coord[0] == self.letter and 0 <= s_coord[1] - self.number <= 2:
            return True
        elif self.colour == 1 and s_coord[0] == self.letter and 0 <= self.number - s_coord[1] <= 2:
            return True
        else:
            return False

    def can_eat(self, square, __, piece, _):
        s_coord = square.give_letter_and_number()
        p_colour = piece.get_colour()

        if ((letter_dict[self.letter] - letter_dict[s_coord[0]] == 1 and s_coord[1] - self.number == 1)
        or (letter_dict[s_coord[0]] - letter_dict[self.letter]  == 1 and s_coord[1] - self.number == 1)
        ) and self.colour == 0 and p_colour != self.colour and not piece.check_king():
            return True

        elif ((letter_dict[s_coord[0]] - letter_dict[self.letter] == 1 and self.number - s_coord[1] == 1)
        or (letter_dict[self.letter] - letter_dict[s_coord[0]] == 1 and self.number - s_coord[1] == 1)
        ) and self.colour == 1 and p_colour != self.colour and not piece.check_king():
            return True
        else:
            return False


class Bishop(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White Bishop.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black Bishop.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)

    def can_move(self, square, old_square, position):
        if square.give_letter_and_number() in old_square.get_diagonals(position):
            return True
        else:
            return False

    def can_eat(self, square, old_square, piece, position):
        if self.can_move(square, old_square, position) and piece.get_colour() != self.colour and not piece.check_king():
            return True
        else:
            return False


class Knight(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White Knight.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black Knight.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)

    def can_move(self, square, old_square, _):
        if square.give_letter_and_number() in old_square.get_horse_moves():
            return True
        else:
            return False

    def can_eat(self, square, old_square, piece, _):
        if self.can_move(square, old_square, _) and piece.get_colour() != self.colour and not piece.check_king():
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White Rook.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black Rook.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)

    def can_move(self, square, old_square, position):
        if square.give_letter_and_number() in old_square.get_verticals(position):
            return True
        else:
            return False

    def can_eat(self, square, old_square, piece, position):
        if self.can_move(square, old_square,position) and piece.get_colour() != self.colour and not piece.check_king():
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White Queen.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black Queen.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)

    def can_move(self, square, old_square, position):
        if square.give_letter_and_number() in old_square.get_verticals(position) \
                or square.give_letter_and_number() in old_square.get_diagonals(position):
            return True
        else:
            return False

    def can_eat(self, square, old_square, piece, position):
        if self.can_move(square, old_square, position) and piece.get_colour() != self.colour and not piece.check_king():
            return True
        else:
            return False


class King(Piece):
    def __init__(self, colour, letter, number, cash_pos=None):
        Piece.__init__(self, colour, letter, number, cash_pos)
        if colour == 0:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/White King.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        else:
            picture = pygame.image.load(r'C:\Users\Рамиль\PycharmProjects\chess\Images' + '/Black King.svg')
            picture = pygame.transform.scale(picture, (70, 66))
            self.image = picture
        self.rect = self.image.get_rect()
        x = -25 + 50 * letter_dict[letter] + 8
        y = 425 - 50 * number + 7
        self.rect.center = (x, y)
        self.is_king = True

    def can_move(self, square, old_square, _):
        if square.give_letter_and_number() in old_square.get_round() and not square.if_attacked(self.colour):
            return True
        else:
            return False

    def can_eat(self, square, old_square, piece, _):
        if self.can_move(square, old_square, _) and piece.get_colour() != self.colour and not piece.check_king():
            return True
        else:
            return False
