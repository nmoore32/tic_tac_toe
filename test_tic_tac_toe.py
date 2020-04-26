"""
Test suite for Tic-Tac-Toe
"""
import unittest

from tic_tac_toe import DRAW, EMPTY, PLAYERO, PLAYERX, TTTBoard


class TestTTT(unittest.TestCase):
    """
    Series of tests for Tic-Tac-Toe
    """

    def setUp(self):
        """
        Create an instance of TTTBoard for each test
        """
        self.game = TTTBoard(3)

    def test_initial_values(self):
        """
        Tests that board initializes correctly
        """
        self.assertEqual(self.game._dim, 3)
        self.assertEqual(self.game._reverse, False)
        self.assertEqual(self.game._board, [[' ', ' ', ' '], [
                         ' ', ' ', ' '], [' ', ' ', ' ']])

    def test_string(self):
        """
        Tests that appropriate string representation of game board is returned
        """
        expected_empty_board_string = '  |   |  \n---------\n  |   |  \n---------\n  |   |  '
        self.assertEqual(str(self.game), expected_empty_board_string)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERX
        expected_x_board_string = 'X | X | X\n---------\nX | X | X\n---------\nX | X | X'
        self.assertEqual(str(self.game), expected_x_board_string)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERO
        expected_o_board_string = 'O | O | O\n---------\nO | O | O\n---------\nO | O | O'
        self.assertEqual(str(self.game), expected_o_board_string)

    def test_get_dim(self):
        """
        Make sure dimension of the board is returned by get_dim()
        """
        self.assertEqual(self.game.get_dim(), self.game._dim)

    def test_get_square(self):
        """
        Make sure the contents of a requested square are returned
        """
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.get_square(row, col), ' ')

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERX
                self.assertEqual(self.game.get_square(row, col), PLAYERX)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERO
                self.assertEqual(self.game.get_square(row, col), PLAYERO)

    def test_get_empty_squares(self):
        """
        Ensures that get_empty_squares returns positions for all and only empty squares
        """
        self.assertEqual(self.game.get_empty_squares(), [
                         (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERX
        self.assertEqual(self.game.get_empty_squares(), [])

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERO
        self.assertEqual(self.game.get_empty_squares(), [])

    def test_get_board(self):
        """
        Ensure that get_board returns an appropriate copy of the board
        """
        copy1 = self.game.get_board()
        self.assertEqual(copy1._board, self.game._board)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERX
        copy2 = self.game.get_board()
        self.assertEqual(copy2._board, self.game._board)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = PLAYERO
        copy3 = self.game.get_board()
        self.assertEqual(copy3._board, self.game._board)

    def test_move(self):
        """
        Ensure that move adds the appropriate player symbol to the board
        only if the selected square is empty
        """
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game.move(row, col, PLAYERX)
                self.assertEqual(self.game.get_square(row, col), PLAYERX)

        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game.move(row, col, PLAYERO)
                self.assertEqual(self.game.get_square(row, col), PLAYERX)
                self.game._board[row][col] = PLAYERO
                self.game.move(row, col, PLAYERO)
                self.assertEqual(self.game.get_square(row, col), PLAYERO)

    def test_check_win(self):
        """
        Ensure that check_win returns appropriate response for various board states
        """
        # Horizontal wins
        # First row
        self.game.move(0, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(0, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(0, 2, PLAYERX)
        self.assertEqual(self.game.check_win(0, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(0, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(0, 2, PLAYERX), PLAYERX)

        # Second row
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(1, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 2, PLAYERX)
        self.assertEqual(self.game.check_win(1, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 2, PLAYERX), PLAYERX)

        # Third row
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(2, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 2, PLAYERX)
        self.assertEqual(self.game.check_win(2, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 2, PLAYERX), PLAYERX)

        # Vertical wins
        # First column
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(0, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 0, PLAYERX)
        self.assertEqual(self.game.check_win(0, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 0, PLAYERX), PLAYERX)

        # Second column
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(0, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 1, PLAYERX)
        self.assertEqual(self.game.check_win(0, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 1, PLAYERX), PLAYERX)

        # Third column
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(0, 2, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 2, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 2, PLAYERX)
        self.assertEqual(self.game.check_win(0, 2, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 2, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 2, PLAYERX), PLAYERX)

        # Diagonal wins
        # Upper left to bottom right
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(0, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 2, PLAYERX)
        self.assertEqual(self.game.check_win(0, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(2, 2, PLAYERX), PLAYERX)

        # Bottom left to upper right
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(2, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(0, 2, PLAYERX)
        self.assertEqual(self.game.check_win(2, 0, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(1, 1, PLAYERX), PLAYERX)
        self.assertEqual(self.game.check_win(0, 2, PLAYERX), PLAYERX)

        # Draw
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.game._board[row][col] = EMPTY

        self.game.move(0, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(0, 1, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(0, 2, PLAYERO)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 0, PLAYERO)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 1, PLAYERO)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(1, 2, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 0, PLAYERX)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 1, PLAYERO)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), None)
        self.game.move(2, 2, PLAYERO)
        for row in range(self.game._dim):
            for col in range(self.game._dim):
                self.assertEqual(self.game.check_win(row, col, PLAYERX), DRAW)


if __name__ == '__main__':
    unittest.main()
