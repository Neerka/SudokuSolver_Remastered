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
    _last_count: int = PrivateAttr(default=0)

    def findValues(self) -> None:
        """
        Find the values of the tiles in the group
        """
        values = [tile.value for tile in self._tiles]
        for tile in self._tiles:
            tile.findInGroup(set(values))
    
    def findUniqueValues(self) -> None:
        """
        Find the unique possible values of the tiles in the group
        """
        values = [tile.possible_values for tile in self._tiles]
        for tile in self._tiles:
            tile.findUniqueCandidatesInGroups(values)

    def checkGroup(self) -> tuple[bool, bool]:
        zeros_count: int = 0
        for tile in self._tiles:
            if tile.value == 0:
                zeros_count += 1
        if zeros_count == self._last_count:
            return False, False
        elif zeros_count > 0:
            self._last_count = zeros_count
            return False, True
        return True, True
    
    def lookAtTileValue(self, tileID: int) -> int:
        for tile in self._tiles:
            if tile.id == tileID:
                return tile.value
        raise ValueError("Tile not found in group")
    
    def lookAtTilePossibleValues(self, tileID: int) -> set[int]:
        for tile in self._tiles:
            if tile.id == tileID:
                return tile.possible_values
        raise ValueError("Tile not found in group")