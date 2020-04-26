"""
Implementation of Tic-Tac-Toe
Allows for reverse Tic-Tac-Toe in which getting three squares
in a row results in a loss
"""
from copy import deepcopy
from random import choice
import sys

import pygame as pg

# Constants to represent states of the board and of individual squares
EMPTY = ' '
PLAYERX = 'X'
PLAYERO = 'O'
DRAW = 'Draw'

# Constants related to display
WIDTH = 960
HEIGHT = 783
MARGIN_X = 203  # Margins are based on board image size
MARGIN_Y = 140
SCREEN_OFFSET = 100  # To account for gap to left and top of board image
SQUARE_SIZE = 218  # Size of squares on board image
SMALL_FONT_SIZE = 25
MEDIUM_FONT_SIZE = 100
LARGE_FONT_SIZE = 200
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (247, 247, 247)
BLACK = (0, 0, 0)

# Directions
RIGHT = 0
DOWN = 1
DOWN_RIGHT = 2
UP_RIGHT = 3

# Offsets for moving through board in a given direction
OFFSETS = {RIGHT: (0, 1),
           DOWN: (1, 0),
           DOWN_RIGHT: (1, 1),
           UP_RIGHT: (-1, 1)}

# Constants for Monte Carlo simulator
NTRIALS = 2500         # Number of trials to run
SCORE_COMP = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


class TTTBoard:
    """
    Class that represents a Tic-Tac-Toe-Board
    """

    def __init__(self, dim, reverse=False, board=None):
        """
        Initialize the board object with the given dimensions and
        whether the game should be reversed
        """
        self._dim = dim
        self._reverse = reverse
        if board is not None:
            self._board = board
        else:
            self._board = [[EMPTY for row in range(dim)] for col in range(dim)]

    def __str__(self):
        """
        Returns string representation of the board
        E.g.
        'X | O | X
         ---------
           | X | O
         ---------
         O |   | X'
        """
        return_string = ''
        for row in range(self._dim):
            for col in range(self._dim):
                if col == 0:
                    return_string = f"{return_string}{self.get_square(row, col)} |"
                elif col < self._dim - 1:
                    return_string = f"{return_string} {self.get_square(row, col)} |"
                elif col == self._dim - 1:
                    return_string = f"{return_string} {self.get_square(row, col)}"
            if row < self._dim - 1:
                return_string = f"{return_string}\n---------\n"
        return return_string

    def get_dim(self):
        """
        Returns the dimensions of the board
        """
        return self._dim

    def get_square(self, row, col):
        """
        Returns the contents of a square on the board
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Returns a list of (row, col) tuples for all empty squares
        """
        return_list = [(row, col) for row in range(self._dim) for col in range(
            self._dim) if self.get_square(row, col) == EMPTY]
        return return_list

    def get_board(self):
        """
        Returns a copy of the board
        """
        return deepcopy(self)

    def move(self, row, col, player):
        """
        Place player marker on the board at position (row, col).
        player should be one of the constants PLAYERX or PLAYERO
        Does nothing if board square is not empty.
        Returns true if a move is made
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player
            return (row, col)

    def check_win(self, row, col, player):
        """
        Takes position and player of last move so we don't check the entire board each time
        Returns a constant associated with the state of them game
            PLAYERX if PLAYERX wins
            PLAYERO if PLAYERO wins
            DRAW if it's a tie
            None if game is still in progress
        """
        # Check each direction from the last move to see if there's a win
        for dummy_direction, offset in OFFSETS.items():
            run_size = 0
            # Check both directions (e.g. up and down, right and left)
            for i in range(-self._dim + 1, self._dim):
                next_pos = (row + i * offset[0], col + i * offset[1])
                # Make sure the indices refer to a location in the grid
                if 0 <= next_pos[0] < self._dim and 0 <= next_pos[1] < self._dim:
                    if self.get_square(next_pos[0], next_pos[1]) == player:
                        run_size += 1
            # Return the winning player depending on whether game is set to reverse
            if run_size == self._dim and not self._reverse:
                return player
            elif run_size == self._dim and self._reverse:
                if player == PLAYERO:
                    return PLAYERX
                else:
                    return PLAYERO
        # Return None if game is still in progress and DRAW if game is tied
        if any(EMPTY in row for row in self._board):
            return None
        else:
            return DRAW


def mc_trial(board, player):
    """
    Plays a game of Tic-Tac-Toe using the current board state as the starting point
    Returns the winner
    """
    comp = player
    other = None
    if comp == PLAYERX:
        other = PLAYERO
    else:
        other = PLAYERX

    trial_winner = None
    in_progress = True
    while in_progress:
        # Alternate between each player, selecting a random move, check for win/draw
        for idx in [comp, other]:
            idx_move = choice(board.get_empty_squares())
            board.move(idx_move[0], idx_move[1], idx)
            if board.check_win(idx_move[0], idx_move[1], idx) is not None:
                trial_winner = board.check_win(idx_move[0], idx_move[1], idx)
                in_progress = False
                break
    return trial_winner


def mc_update_scores(scores, board, player, winner):
    """
    Takes a grid of scores with the same dimensions as the Tic-Tac-Toe board, the
    computer player, and the winner of a trial. Updates scores for each position.

    Positions of the winning player have their scores increased whereas positions
    of the losing player have their scores decreases.

    No scoring is done if the game is a draw.
    """
    if winner == DRAW:
        return

    # This block here is only needed if we want different scoring values for
    # the winner and loser
    winner_increment = None
    loser_decrement = None
    if winner == player:
        winner_increment = SCORE_COMP
        loser_decrement = SCORE_OTHER
    else:
        winner_increment = SCORE_OTHER
        loser_decrement = SCORE_COMP

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.get_square(row, col) == winner:
                scores[row][col] += winner_increment
            elif board.get_square(row, col) != (winner and EMPTY):
                scores[row][col] -= loser_decrement


def get_best_move(board, scores):
    """
    Determines the best move given the current board and scoring from the Monte Carlo trials
    """
    # Determine the highest scoring empty square
    max_score = 0
    for pos in board.get_empty_squares():
        if scores[pos[0]][pos[1]] > max_score:
            max_score = scores[pos[0]][pos[1]]

    # Make a list of empty squares that have the max_score
    best_empty_squares = [pos for pos in board.get_empty_squares(
    ) if scores[pos[0]][pos[1]] == max_score]

    return choice(best_empty_squares)


def mc_move(board, player, trials):
    """
    Determines the best move based on repeated simulations
    """
    scores = [[0 for row in range(board.get_dim())]
              for col in range(board.get_dim())]
    while trials > 0:
        clone = board.get_board()
        winner = mc_trial(clone, player)
        mc_update_scores(scores, clone, player, winner)
        trials -= 1
    return get_best_move(board, scores)


def draw(screen, board, board_image, board_rects, button_rects, text, winner):
    """
    Draws the current board state
    """
    # Draw the board
    screen.fill(GRAY)
    screen.blit(board_image, (100, 100))
    x_width, x_height = text[0].get_rect().width, text[0].get_rect().height
    o_width, o_height = text[1].get_rect().width, text[1].get_rect().height

    # Draw any X's and O's
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            # The X's and O's have different dimensions, hence why
            # I'm determining their positions separately
            if board.get_square(row, col) == PLAYERX:
                pos_x = board_rects[row][col].x + \
                    (SQUARE_SIZE - x_width) // 2
                # Because the middle squares on the board image are smaller
                # than the others I couldn't position everything correctly
                # horizonally and vertically without using a "random" offset
                # namely, the factor of 0.85
                pos_y = board_rects[row][col].y + \
                    (SQUARE_SIZE - 0.85 * x_height) // 2
                screen.blit(text[0], (pos_x, int(pos_y)))  # blit expects ints
            elif board.get_square(row, col) == PLAYERO:
                pos_x = board_rects[row][col].x + \
                    (SQUARE_SIZE - o_width) // 2
                pos_y = board_rects[row][col].y + \
                    (SQUARE_SIZE - 0.85 * o_height) // 2
                screen.blit(text[1], (pos_x, int(pos_y)))

    # Draw buttons
    for idx, rect in enumerate(button_rects):
        screen.blit(text[idx + 2], rect)

    # If the game is over draw result message
    font = pg.font.Font('freesansbold.ttf', MEDIUM_FONT_SIZE)
    result = None
    if winner == PLAYERX:
        result = 'X wins'
    elif winner == PLAYERO:
        result = 'O wins'
    elif winner == DRAW:
        result = 'Draw'
    result_text = font.render(result, True, BLACK)
    pos_x = SCREEN_OFFSET + (WIDTH - SCREEN_OFFSET -
                             result_text.get_rect().width) // 2
    pos_y = 10  # Just so its not right at the top of the screen
    screen.blit(result_text, (pos_x, pos_y))

    pg.display.flip()


def reset_game(reverse):
    """
    Resets the game
    """
    board = TTTBoard(3, reverse)
    return board


def main():
    """
    Run the game
    """
    pg.init()

    # Create screen and load game assets
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    board_image = pg.image.load('game_board.png')

    # Create font objects for X's and O's
    font_large = pg.font.Font('freesansbold.ttf', LARGE_FONT_SIZE)
    text_x = font_large.render('X', True, BLUE)
    text_o = font_large.render('O', True, RED)

    board = TTTBoard(3)

    # Create Rect objects for the board squares
    board_rects = [[pg.Rect(MARGIN_X + row * SQUARE_SIZE, MARGIN_Y +
                            col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    for row in range(board.get_dim())] for col in range(board.get_dim())]

    # Create Rect objects for buttons
    font_small = pg.font.Font('freesansbold.ttf', SMALL_FONT_SIZE)
    new_game_text = font_small.render('New Game', True, BLACK)
    new_game_rect = new_game_text.get_rect()
    new_game_rect.x, new_game_rect.y = SMALL_FONT_SIZE // 2, SMALL_FONT_SIZE // 2

    switch_text = font_small.render('Switch Symbol', True, BLACK)
    switch_rect = switch_text.get_rect()
    switch_rect.x, switch_rect.y = SMALL_FONT_SIZE // 2, SMALL_FONT_SIZE // 2 + MARGIN_Y

    reverse_text = font_small.render('Reverse', True, BLACK)
    reverse_rect = reverse_text.get_rect()
    reverse_rect.x, reverse_rect.y = SMALL_FONT_SIZE // 2, SMALL_FONT_SIZE // 2 + 2 * MARGIN_Y
    button_rects = [new_game_rect, switch_rect, reverse_rect]

    # Create a tuple of all the text objects to pass to the draw method
    texts = (text_x, text_o, new_game_text, switch_text, reverse_text)

    # Initial some varibles for book keeping
    winner = None
    player_turn = False
    player_move = None
    reverse = False
    comp = PLAYERX
    player = PLAYERO

    # Main game logic
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                coords = event.pos
                # The new_game, switch, and reverse buttons don't do anything
                # if a game is in progress
                if new_game_rect.collidepoint(coords) and winner is not None:
                    board = reset_game(reverse)
                    winner = None
                    player_move = None
                    # Sets the player to go first if they're X
                    if player == PLAYERX:
                        player_turn = True
                elif switch_rect.collidepoint(coords) and winner is not None:
                    temp = player
                    player = comp
                    comp = temp
                elif reverse_rect.collidepoint(coords) and winner is not None:
                    reverse = not reverse
                for row in range(board.get_dim()):
                    for col in range(board.get_dim()):
                        if board_rects[row][col].collidepoint(coords):
                            player_move = (row, col)
                            break

        draw(screen, board, board_image, board_rects, button_rects, texts, winner)

        if not player_turn and not winner:
            comp_move = mc_move(board, comp, NTRIALS)
            board.move(comp_move[0], comp_move[1], comp)
            result = board.check_win(comp_move[0], comp_move[1], comp)
            if result is not None:
                winner = result
            else:
                player_turn = True
        elif player_move and not winner:
            # Only update if the call to move returns a result
            # this prevents clicking on a filled space from counting as a move
            if board.move(player_move[0], player_move[1], player):
                result = board.check_win(
                    player_move[0], player_move[1], player)
                player_move = None
                player_turn = False
                if result is not None:
                    winner = result


if __name__ == '__main__':
    main()
