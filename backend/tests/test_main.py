import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tile import Tile
from column import Column

def test_tile():
    column = Column(id=0)
    tile = Tile(id=0, column = column)
    assert tile.id == 0
    assert tile.value == 0
    assert tile.model_dump() == {
        "id": 0,
        "value": 0
    }