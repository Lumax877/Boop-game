import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
ROWS, COLS = 6, 6
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FONT_COLOR = (0, 0, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boop - Game")

CAT_RADIUS_SMALL = SQUARE_SIZE // 4
CAT_RADIUS_LARGE = SQUARE_SIZE // 3
INFO_BAR_HEIGHT = 100

cats_in_hand = {
    1: {'small': 8, 'large': 0},
    2: {'small': 8, 'large': 0}
}

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

selected_piece = 'small'


def draw_board():
    if selected_piece == "small":
        catsize = "small"
    else:
        catsize = "big"
    WIN.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            if board[row][col] == 1:
                pygame.draw.circle(WIN, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CAT_RADIUS_SMALL)
            elif board[row][col] == 2:
                pygame.draw.circle(WIN, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CAT_RADIUS_SMALL)
            elif board[row][col] == 3:
                pygame.draw.circle(WIN, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CAT_RADIUS_LARGE)
            elif board[row][col] == 4:
                pygame.draw.circle(WIN, RED,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CAT_RADIUS_LARGE)

    pygame.draw.rect(WIN, WHITE, (0, HEIGHT - INFO_BAR_HEIGHT, WIDTH, INFO_BAR_HEIGHT))
    pygame.draw.line(WIN, BLACK, (0, HEIGHT - INFO_BAR_HEIGHT), (WIDTH, HEIGHT - INFO_BAR_HEIGHT), 2)

    font = pygame.font.Font(None, 36)
    text1 = font.render(f"Gracz 1 koty: {cats_in_hand[1]['small']}", True, FONT_COLOR)
    text2 = font.render(f"Gracz 2 koty: {cats_in_hand[2]['small']}", True, FONT_COLOR)
    text3 = font.render(f"Gracz 1 duże koty: {cats_in_hand[1]['large']}", True, FONT_COLOR)
    text4 = font.render(f"Gracz 2 duże koty: {cats_in_hand[2]['large']}", True, FONT_COLOR)
    text5 = font.render(f"Tura gracza: {player}", True, FONT_COLOR)
    text6 = font.render(f"Wybrany kot: {catsize}", True, FONT_COLOR)
    WIN.blit(text1, (10, HEIGHT - INFO_BAR_HEIGHT + 10))
    WIN.blit(text2, (WIDTH // 2 + 10, HEIGHT - INFO_BAR_HEIGHT + 10))
    WIN.blit(text3, (10, HEIGHT - INFO_BAR_HEIGHT + 40))
    WIN.blit(text4, (WIDTH // 2 + 10, HEIGHT - INFO_BAR_HEIGHT + 40))
    WIN.blit(text5, (10, HEIGHT - INFO_BAR_HEIGHT + 70))
    WIN.blit(text6, (WIDTH // 2 + 10, HEIGHT - INFO_BAR_HEIGHT + 70))

    pygame.display.update()


def get_square_under_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def move_cat(row, col, player, piece_type):
    if board[row][col] == 0 and cats_in_hand[player][piece_type] > 0:
        if piece_type == 'small':
            board[row][col] = player
        elif piece_type == 'large':
            board[row][col] = player + 2
        cats_in_hand[player][piece_type] -= 1
        push_around(row, col)
        check_three_in_a_row(player)


def push_around(row, col):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # nie pytajcie XD
            if dx == 0 and dy == 0:
                continue
            new_row, new_col = row + dy, col + dx
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:

                if board[new_row][new_col] != 0:
                    push_opposite(row, col, new_row, new_col)


def push_opposite(pushing_row, pushing_col, pushed_row, pushed_col):
    dx = pushed_col - pushing_col
    dy = pushed_row - pushing_row

    pushing_piece = board[pushing_row][pushing_col]
    pushed_piece = board[pushed_row][pushed_col]

    if pushing_piece in [1, 2] and pushed_piece in [3, 4]:
        return  # Mały kot nie może popychać dużego kota

    target_row = pushed_row + dy
    target_col = pushed_col + dx

    if 0 <= target_row < ROWS and 0 <= target_col < COLS:
        if board[target_row][target_col] == 0:
            board[target_row][target_col] = pushed_piece
            board[pushed_row][pushed_col] = 0
    else:

        if pushed_piece == 1:
            cats_in_hand[1]['small'] += 1
        elif pushed_piece == 2:
            cats_in_hand[2]['small'] += 1
        elif pushed_piece == 3:
            cats_in_hand[1]['large'] += 1
        elif pushed_piece == 4:
            cats_in_hand[2]['large'] += 1

        board[pushed_row][pushed_col] = 0


def check_three_in_a_row(player):
    for row in range(ROWS):
        for col in range(COLS - 2):  # Maksymalna długość linii poziomej to COLS - 2
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player:
                remove_three_cats(row, col, row, col + 1, row, col + 2, player)

    for col in range(COLS):
        for row in range(ROWS - 2):  # Maksymalna długość linii pionowej to ROWS - 2
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player:
                remove_three_cats(row, col, row + 1, col, row + 2, col, player)

    for row in range(ROWS - 2):
        for col in range(COLS - 2):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player:
                remove_three_cats(row, col, row + 1, col + 1, row + 2, col + 2, player)

    for row in range(2, ROWS):
        for col in range(COLS - 2):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player:
                remove_three_cats(row, col, row - 1, col + 1, row - 2, col + 2, player)


def remove_three_cats(row1, col1, row2, col2, row3, col3, player):
    board[row1][col1] = 0
    board[row2][col2] = 0
    board[row3][col3] = 0
    cats_in_hand[player]['small'] += 2
    cats_in_hand[player]['large'] += 1


def main():
    global player
    player = 1
    running = True
    global selected_piece
    while running:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    selected_piece = 'small'
                    print("small")
                if event.key == pygame.K_b:
                    selected_piece = 'large'
                    print("big")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    row, col = get_square_under_mouse(pos)
                    if board[row][col] == 0 and cats_in_hand[player][selected_piece] > 0:
                        move_cat(row, col, player, selected_piece)
                        check_three_in_a_row(player)
                        player = 3 - player


main()

# TODO: winning condition
# TODO: line detection logic when big cat is involved
# TODO: row-longer-than-3 handling?