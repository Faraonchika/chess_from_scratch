import pygame
from Board import Board
from Pieces import Pawn, Bishop, Knight, Rook, Queen, King
from Rules import next_move


# Initial params
WIDTH = 400  # width of game screen
HEIGHT = 400  # height of game screen
FPS = 60
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Colours (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen preparations
pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Chess")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# Board init
board = Board()
board.start_pos()

figs = [Rook(0, 'A', 1, 0), Knight(0, 'B', 1, 1), Bishop(0, 'C', 1, 2), Queen(0, 'D', 1, 3), King(0, 'E', 1, 4),
            Bishop(0, 'F', 1, 5), Knight(0, 'G', 1, 6), Rook(0, 'H', 1, 7)] + [Pawn(0, letters[i], 2,
                                                                                    7 + 1 + i) for i in range(8)] + \
           [Rook(1, 'A', 8, 16), Knight(1, 'B', 8, 17), Bishop(1, 'C', 8, 18), Queen(1, 'D', 8, 19),
            King(1, 'E', 8, 20), Bishop(1, 'F', 8, 21), Knight(1, 'G', 8, 22), Rook(1, 'H', 8, 23)] + \
       [Pawn(1, letters[i], 7,
             23 + 1 + i) for i in range(8)]

# Put Pieces on Board
for piece in figs:
    piece.put_on_board(board)

# Game cycle
running = True
took_piece = None
old_square = None
turn = 0
print(board.position[0][4])
kings_pos = [board.position[0][4], board.position[0][7]]
kings_checks = [False, False]
kings_threats = [[], []]
while running:
    # Correct speed of cycle
    clock.tick(FPS)
    # Event input

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
            if len(clicked_sprites) == 2 and took_piece is None:
                took_piece = clicked_sprites[-1]
                old_square = clicked_sprites[0]
                if took_piece.cash_pos == 5:
                    print(took_piece.square.get_diagonals(board.position))
                if took_piece.get_colour() != turn:
                    took_piece = None
                    old_square = None

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
            s = clicked_sprites[0]

            # Move the piece
            if len(clicked_sprites) == 2 and took_piece is not None:
                if took_piece.can_move(s, old_square, board.position):
                    new_pos = s.give_letter_and_number()
                    if new_pos != old_square.give_letter_and_number():
                        figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                        board.square_piece_put(s)
                        board.square_piece_gone(old_square)
                        took_piece.move_on_board(s)

                        # change attacked squares
                        if turn == 0:
                            board.refresh_attacks(figs[:16], turn)
                        else:
                            board.refresh_attacks(figs[16:], turn)

                        # check for king
                        if took_piece.is_king:
                            kings_pos[turn] = s
                            print(kings_pos)

                        # check for the check
                        if took_piece.can_move(kings_pos[next_move(turn)], s, board.position):
                            kings_checks[next_move(turn)] = True
                            kings_threats[next_move(turn)].append(took_piece)
                            print(kings_checks, kings_threats)

                        took_piece = None
                        old_square = None

                        board.get_attack_mat(turn)
                        board.get_pieces_mat()

                        # Rules Applied
                        turn = next_move(turn)

                        # Sound Effect
                        pygame.mixer.music.load('Sounds/piece_move.wav')
                        pygame.mixer.music.play()

                    else:
                        new_pos = old_square.give_letter_and_number()
                        figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                        took_piece = None
                        old_square = None
                else:
                    new_pos = old_square.give_letter_and_number()
                    figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                    took_piece = None
                    old_square = None

            # Take other piece
            elif len(clicked_sprites) == 3 and took_piece is not None:
                fig_to_delete = None
                for cl in clicked_sprites:
                    if cl.name != "Square" and cl != took_piece:
                        fig_to_delete = cl

                if took_piece.can_eat(s, old_square, fig_to_delete, board.position):
                    new_pos = s.give_letter_and_number()
                    figs[fig_to_delete.cash_pos].delete_piece()
                    figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                    board.square_piece_put(s)
                    board.square_piece_gone(old_square)
                    took_piece.move_on_board(s)

                    # change attacked squares
                    if turn == 0:
                        board.refresh_attacks(figs[:16], turn)
                    else:
                        board.refresh_attacks(figs[16:], turn)

                    # check for king
                    if took_piece.is_king:
                        kings_pos[turn] = s
                        print(kings_pos)

                    # check for the check
                    if took_piece.can_move(kings_pos[next_move(turn)], s, board.position):
                        kings_checks[next_move(turn)] = True
                        kings_threats[next_move(turn)].append(took_piece)
                        print(kings_checks, kings_threats)

                    took_piece = None
                    old_square = None

                    board.get_attack_mat(turn)
                    board.get_pieces_mat()

                    # Rules Applied
                    turn = next_move(turn)

                    # Sound Effect
                    pygame.mixer.music.load('Sounds/piece_eat.wav')
                    pygame.mixer.music.play()

                else:
                    new_pos = old_square.give_letter_and_number()
                    figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                    took_piece = None
                    old_square = None

            elif len(clicked_sprites) > 3 and took_piece is not None:
                new_pos = old_square.give_letter_and_number()
                figs[took_piece.cash_pos].change_place(new_pos[0], new_pos[1])
                took_piece = None
                old_square = None

        if pygame.mouse.get_pressed()[0] and took_piece is not None and took_piece.get_colour() == turn:
            pos = pygame.mouse.get_pos()
            figs[took_piece.cash_pos].move_freely(pos[0] + 5, pos[1])

    # update
    all_sprites.update()

    for line in board.position:
        for s in line:
            all_sprites.add(s)
    for f in figs:
        if f.can_draw():
            all_sprites.add(f)
        else:
            all_sprites.remove(f)

    # Rendering
    screen.fill(BLACK)

    # After drawing we flip th screen
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
