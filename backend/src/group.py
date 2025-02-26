from pydantic import BaseModel, Field, PrivateAttr
from boardStructure import BoardStructure
from tile import Tile

class Group(BoardStructure):
    """
    The group class has the following attributes:
    - id: the index of the group (0-8, left to right)
    - tiles: the tiles in the group
    """
    _type: str = "Group"

    def findValues(self) -> None:
        """
        Find the values of the tiles in the group
        """
        values = [tile.value for tile in self._tiles]
        for tile in self._tiles:
            tile.findInGroup(values)
    
    def findUniqueValues(self) -> None:
        """
        Find the unique possible values of the tiles in the group
        """
        values = [tile.possible_values for tile in self._tiles]
        for tile in self._tiles:
            tile.findUniqueInGroup(values)