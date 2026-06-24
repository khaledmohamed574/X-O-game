"""Quick logic tests for tic_tac_toc_game (no input required)."""
import importlib.util
import sys
from pathlib import Path

_game_path = Path(__file__).parent / "X-O_game.py"
_spec = importlib.util.spec_from_file_location("xo_game", _game_path)
_xo_game = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_xo_game)

Board = _xo_game.Board
Game = _xo_game.Game

def test_board_starts_with_numbers():
    b = Board()
    assert b.board == [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]


def test_all_cell_positions():
    """Each input 1-9 maps to the correct board cell."""
    b = Board()
    expected = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2),
    }
    for choice, (row, col) in expected.items():
        assert b.choice_to_position(choice) == (row, col)
        assert b.position_to_choice(row, col) == choice
        assert b.is_valid_move(choice)
        assert b.update_board(choice, str(choice))
        assert b.board[row][col] == str(choice)


def test_board_valid_move_and_update():
    b = Board()
    # Cells 1-9 map to flat index; current code uses choice-1 as row index
    assert b.is_valid_move(1), "cell 1 should be available"
    ok = b.update_board(1, "X")
    assert ok, "first move should succeed"
    assert b.board[0][0] == "X", f"expected cell 1 to be 'X', got {b.board[0][0]}"


def test_check_win_rows():
    g = Game()
    # Row win: top row all X
    g.board.board = [["X", "X", "X"], ["4", "5", "6"], ["7", "8", "9"]]
    result = g.check_win()
    assert result is True, f"row win should be True, got {result}"


def test_check_win_diagonal():
    g = Game()
    g.board.board = [["X", "2", "3"], ["4", "X", "6"], ["7", "8", "X"]]
    assert g.check_win() is True, "diagonal win should be True"


def test_check_draw():
    g = Game()
    g.board.board = [["X", "O", "X"], ["O", "O", "X"], ["O", "X", "O"]]
    result = g.check_draw()
    assert result is True, f"full board no winner should be draw, got {result}"


def test_no_false_win():
    g = Game()
    g.board.board = [["X", "O", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    assert g.check_win() is False, "no win yet"


if __name__ == "__main__":
    tests = [
        test_board_starts_with_numbers,
        test_all_cell_positions,
        test_board_valid_move_and_update,
        test_check_win_rows,
        test_check_win_diagonal,
        test_check_draw,
        test_no_false_win,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL: {t.__name__} -> {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
