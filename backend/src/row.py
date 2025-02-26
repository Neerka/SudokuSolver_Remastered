from pydantic import BaseModel, Field
from boardStructure import BoardStructure
from tile import Tile

class Row(BoardStructure):
    """
    The row class has the following attributes:
    - id: the index of the row (0-8, left to right)
    - tiles: the tiles in the row
    """
    _type: str = "Row"

    def findValues(self) -> None:
        """
        Find the values of the tiles in the row
        """
        values = [tile for tile in self._tiles]
        for tile in self._tiles:
            tile.findInRow(values)

    def findUniqueValues(self) -> None:
        """
        Find the unique possible values of the tiles in the row
        """
        values = [tile.possible_values for tile in self._tiles]
        for tile in self._tiles:
            tile.findUniqueInRow(values)
        