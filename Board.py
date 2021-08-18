import pygame
from Functions import give_2d_pos
from Rules import next_move
from Pieces import Piece


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
letter_dict_rev = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}


class Square(pygame.sprite.Sprite):
    def __init__(self, s_type, x, y, cash_pos=None, has_piece=False, white_or_black=(False, False)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        if s_type == 0:
            self.image.fill(WHITE)
        elif s_type == 1:
            self.image.fill(BLACK)
        else:
            print("Error")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cash_pos = cash_pos
        self.name = 'Square'
        self.has_piece = has_piece
        self.white_or_black = white_or_black

    def piece_gone(self):
        self.has_piece = False

    def piece_put(self):
        self.has_piece = True

    def give_letter_and_number(self):
        return letters[self.rect.center[0] // 50], abs(425 - self.rect.center[1]) // 50

    def not_attacked(self, turn):
        if turn == 0:
            self.white_or_black = (False, self.white_or_black[1])
        else:
            self.white_or_black = (self.white_or_black[0], False)

    def attacked(self, turn):
        if turn == 0:
            self.white_or_black = (True, self.white_or_black[1])
        else:
            self.white_or_black = (self.white_or_black[0], True)

    def if_attacked(self, turn):
        return self.white_or_black[next_move(turn)]

    def get_diagonals(self, position):
        letter, number = self.give_letter_and_number()
        letter = letters.index(letter) + 1
        diagonals = []

        got_piece = False
        x, y = letter, number
        while x > 1 and y > 1 and not got_piece:
            x -= 1
            y -= 1
            if position[y - 1][x - 1].has_piece:
                diagonals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                diagonals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while x < 8 and y < 8 and not got_piece:
            x += 1
            y += 1
            if position[y - 1][x - 1].has_piece:
                diagonals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                diagonals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while x > 1 and y < 8 and not got_piece:
            x -= 1
            y += 1
            if position[y - 1][x - 1].has_piece:
                diagonals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                diagonals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while x < 8 and y > 1 and not got_piece:
            x += 1
            y -= 1
            if position[y - 1][x - 1].has_piece:
                diagonals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                diagonals.append((letter_dict_rev[x], y))
        return diagonals

    def get_verticals(self, position):
        letter, number = self.give_letter_and_number()
        letter = letters.index(letter) + 1
        verticals = []

        got_piece = False
        x, y = letter, number
        while x > 1 and not got_piece:
            x -= 1
            if position[y - 1][x - 1].has_piece:
                verticals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                verticals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while x < 8 and not got_piece:
            x += 1
            if position[y - 1][x - 1].has_piece:
                verticals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                verticals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while y < 8 and not got_piece:
            y += 1
            if position[y - 1][x - 1].has_piece:
                verticals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                verticals.append((letter_dict_rev[x], y))

        got_piece = False
        x, y = letter, number
        while y > 1 and not got_piece:
            y -= 1
            if position[y - 1][x - 1].has_piece:
                verticals.append((letter_dict_rev[x], y))
                got_piece = True
            else:
                verticals.append((letter_dict_rev[x], y))

        return verticals

    def get_horse_moves(self):
        letter, number = self.give_letter_and_number()
        letter = letters.index(letter) + 1
        moves = []

        x, y = letter + 2, number + 1
        if x <= 8 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 1, number + 2
        if x <= 8 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 2, number - 1
        if x >= 1 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 1, number - 2
        if x >= 1 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 2, number - 1
        if x <= 8 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 1, number - 2
        if x <= 8 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 2, number + 1
        if x >= 1 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 1, number + 2
        if x >= 1 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        return moves

    def get_round(self):
        letter, number = self.give_letter_and_number()
        letter = letters.index(letter) + 1
        moves = []

        x, y = letter, number + 1
        if x <= 8 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 1, number + 1
        if x <= 8 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 1, number
        if x <= 8 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        x, y = letter + 1, number - 1
        if x <= 8 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter, number - 1
        if x >= 1 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 1, number - 1
        if x >= 1 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 1, number
        if x >= 1 and y >= 1:
            moves.append((letter_dict_rev[x], y))

        x, y = letter - 1, number + 1
        if x >= 1 and y <= 8:
            moves.append((letter_dict_rev[x], y))

        return moves


class Board:
    def __init__(self):
        self.position = None

    def square_piece_gone(self, square):
        i, j = give_2d_pos(self.position, square)
        self.position[i][j].piece_gone()

    def square_piece_put(self, square):
        i, j = give_2d_pos(self.position, square)
        self.position[i][j].piece_put()

    def has_piece(self, letter, number):
        return self.position[letters.index(letter)][number-1].has_piece

    def get_attack_mat(self, turn):
        for line in reversed(self.position):
            for_print = []
            for square in line:
                a = square.if_attacked(next_move(turn))
                if a:
                    for_print.append(1)
                else:
                    for_print.append(0)
            print(for_print)
        print()
        print()

    def get_pieces_mat(self):
        for line in reversed(self.position):
            for_print = []
            for square in line:
                a = square.has_piece
                if a:
                    for_print.append(1)
                else:
                    for_print.append(0)
            print(for_print)
        print()
        print()

    def clear_attacks(self, turn):
        for line in range(8):
            for square in range(8):
                self.position[line][square].not_attacked(turn)

    def refresh_attacks(self, pieces, turn):
        self.clear_attacks(turn)
        for piece in pieces:
            for line in range(8):
                for square in range(8):
                    if piece.is_pawn:
                        if piece.can_eat(self.position[line][square], 0, Piece(
                                next_move(turn), letters[square], line+1), 0):
                            self.position[line][square].attacked(turn)
                    else:
                        if piece.can_eat(self.position[line][square], piece.square, Piece(
                                next_move(turn), letters[square], line+1), self.position):
                            self.position[line][square].attacked(turn)

    def start_pos(self):
        pos = []
        y = 425
        for j in range(8):
            y -= 50
            x = -25
            line = []
            for i in range(8):
                x += 50
                if j % 2 > 0 and i % 2 > 0:
                    if j <= 1 or j >= 6:
                        line.append(Square(1, x, y, 8*j + i, True))
                    elif j == 2:
                        line.append(Square(1, x, y, 8 * j + i, False, (True, False)))
                    elif j == 5:
                        line.append(Square(1, x, y, 8 * j + i, False, (False, True)))
                    else:
                        line.append(Square(1, x, y, 8 * j + i, False))
                elif j % 2 > 0 and i % 2 == 0:
                    if j <= 1 or j >= 6:
                        line.append(Square(0, x, y, 8*j + i, True))
                    elif j == 2:
                        line.append(Square(0, x, y, 8 * j + i, False, (True, False)))
                    elif j == 5:
                        line.append(Square(0, x, y, 8 * j + i, False, (False, True)))
                    else:
                        line.append(Square(0, x, y, 8 * j + i, False))
                elif j % 2 == 0 and i % 2 > 0:
                    if j <= 1 or j >= 6:
                        line.append(Square(0, x, y, 8*j + i, True))
                    elif j == 2:
                        line.append(Square(0, x, y, 8 * j + i, False, (True, False)))
                    elif j == 5:
                        line.append(Square(0, x, y, 8 * j + i, False, (False, True)))
                    else:
                        line.append(Square(0, x, y, 8 * j + i, False))
                elif j % 2 == 0 and i % 2 == 0:
                    if j <= 1 or j >= 6:
                        line.append(Square(1, x, y, 8*j + i, True))
                    elif j == 2:
                        line.append(Square(1, x, y, 8 * j + i, False, (True, False)))
                    elif j == 5:
                        line.append(Square(1, x, y, 8 * j + i, False, (False, True)))
                    else:
                        line.append(Square(1, x, y, 8 * j + i, False))
                else:
                    raise ValueError("Some error in square generation!")
            pos.append(line)
        self.position = pos
