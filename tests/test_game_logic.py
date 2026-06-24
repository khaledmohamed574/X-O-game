import os
import sys

# ensure project root is on sys.path so tests can import `main`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Board, Game


def test_board_update_and_valid_move():
    b = Board()
    assert b.is_valid_move(1)
    assert b.update_board(1, 'X')
    assert b.board[0] == 'X'
    assert not b.is_valid_move(1)


def test_reset_board():
    b = Board()
    b.update_board(1, 'X')
    b.reset_board()
    assert all(cell == " " for cell in b.board)


def test_check_win_row():
    g = Game()
    g.board.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    assert g.check_win()


def test_check_win_col():
    g = Game()
    g.board.board = ['O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ']
    assert g.check_win()


def test_check_win_diag():
    g = Game()
    g.board.board = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
    assert g.check_win()


def test_check_draw():
    g = Game()
    g.board.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'O']
    assert g.check_draw()


def test_no_false_win():
    g = Game()
    g.board.board = ['X', 'O', 'X', 'X', 'O', 'O', ' ', ' ', ' ']
    assert not g.check_win()
    assert not g.check_draw()
