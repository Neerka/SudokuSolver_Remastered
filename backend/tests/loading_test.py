import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from boardCreator import BoardCreator

def test_sudokuCreator():
    board_src = "backend/test_resources/sample1.in"
    sudoku = BoardCreator(board_src)

    assert sudoku.board is not None
    assert sudoku.lookAtTileValue(0) is not None
    assert sudoku.lookAtTileValue(0) == 5
    assert sudoku.lookAtTileValue(1) == 0

    
