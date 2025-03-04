import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tile import Tile
from column import Column
from boardCreator import BoardCreator

def test_tile():
    column = Column(id=0)
    tile = Tile(id=0)
    assert column.id == 0
    assert tile.id == 0
    assert tile.value == 0
    tile.model_dump() == {
        "id": 0,
        "tile_value": 0
    }

def test_solving():
    board_src = "backend/test_resources/sample2.in"
    board_wynik = "backend/test_resources/sample2.exp"
    sudoku = BoardCreator(board_src)
    sudoku.createBoard(0)

    values = []
    for line in open(board_wynik):
        line = line.strip()
        for item in line:
            item = int(item)
            values.append(item)

    assert sudoku.solveBoard() is None
    for i in range(81):
        assert sudoku.lookAtTileValue(i) == values[i]
    # assert sudoku.lookAtTileValue(1) == 1
    # assert sudoku.lookAtTileValue(12) == 8