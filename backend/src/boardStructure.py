from pydantic import BaseModel, Field, PrivateAttr
from tile import Tile
from itertools import combinations

class BoardStructure(BaseModel):
    id: int
    _type: str = PrivateAttr()
    _tiles: list[Tile] = PrivateAttr(default=[])
    _possible_values_map: dict = PrivateAttr(default={})
    _possible_values_reverse_map: dict = PrivateAttr(default={})

    @property
    def tiles(self) -> list[Tile]:
        return self._tiles
    
    def addTile(self, tile: Tile) -> None:
        """
        Add a tile to the board element
        """
        if len(self._tiles) >= 9:
            raise ValueError(f"{self._type} {self.id} already has 9 tiles")
        self._tiles.append(tile)

    def updateTiles(self) -> None:
        """
        Update the tiles in the board element
        """
        for tile in self._tiles:
            tile.update()

    def redundantNormalCommonValues(self) -> None:
        map: dict = {}

        for tile in self._tiles:
            if tile.possible_values not in map.keys():
                map[tile.possible_values] = 1
            else:
                map[tile.possible_values] += 1

        for key, value in map.items():
            if len(key) == value:
                [tile.removeCommon(key) for tile in self._tiles]
        
    def mapPossibleValues(self) -> None:
        for tile in self._tiles:
            for value in tile.possible_values:
                self._possible_values_map[value] = self._possible_values_map[value] + 1 if value in self._possible_values_map.keys() else 1

    def reverseMappedValues(self) -> None:
        for key, value in self._possible_values_map.items():
            self._possible_values_reverse_map[value] = set([key]) if value not in self._possible_values_reverse_map else self._possible_values_reverse_map[value] + set([key])

    def findAndClearHiddenCommon(self) -> None:
        self.mapPossibleValues()
        self.reverseMappedValues()

        for key, value in self._possible_values_reverse_map.items():
            combination_set: set[set[int]] = combinations(value, key)
            for combination in combination_set:
                counter: int = 0
                combination = set(combination)
                for tile in self._tiles:
                    counter += 1 if tile.findHidden(combination) else 0
                if counter == key:
                    [tile.clearHidden(combination) for tile in self._tiles]
        