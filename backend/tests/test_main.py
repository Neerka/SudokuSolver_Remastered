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
    board_src = "backend/test_resources/sample1.in"
    board_wynik = "backend/test_resources/sample1.exp"
    creator = BoardCreator()
    board = creator.createBoard(board_src, 0)

    values = []
    for line in open(board_wynik):
        line = line.strip()
        for item in line:
            item = int(item)
            values.append(item)

    
    assert board.solve() is True
    for i in range(81):
        assert board.lookAtTileValue(i) == values[i]