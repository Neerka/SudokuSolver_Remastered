from pydantic import BaseModel, Field, PrivateAttr
from boardStructure import BoardStructure
from tile import Tile

class Column(BoardStructure):
    """
    The column class has the following attributes:
    - id: the index of the column (0-8, left to right)
    - tiles: the tiles in the column
    """
    _type: str = "Column"

    def findValues(self) -> None:
        """
        Find the values of the tiles in the column
        """
        values = [tile.value for tile in self._tiles]
        for tile in self._tiles:
            tile.findInColumn(set(values))

    def findUniqueValues(self) -> None:
        """
        Find the unique possible values of the tiles in the column
        """
        values = [tile.possible_values for tile in self._tiles]
        for tile in self._tiles:
            tile.findUniqueCandidatesInColumns(values)