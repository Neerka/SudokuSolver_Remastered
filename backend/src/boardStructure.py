from pydantic import BaseModel, Field, PrivateAttr
from tile import Tile
from itertools import combinations
from dataTransform import fromIntSetToString, fromStringToIntSet

class BoardStructure(BaseModel):
    id: int
    _type: str = PrivateAttr()
    _tiles: list[Tile] = PrivateAttr(default=[])
    _possible_values_map: dict[int: int] = PrivateAttr(default=dict())
    _possible_values_reverse_map: dict[int: set[int]] = PrivateAttr(default=dict())

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
        # print(map)
        for tile in self._tiles:
            possible: set[int] = tile.possible_values
            # print(type(possible))
            if possible:
                key: str = fromIntSetToString(possible)
                if key not in map.keys():
                    map[key] = 1
                else:
                    map[key] += 1
        # print("Commiting normal pair reduction")
        for key, value in map.items():
            if len(key) == value:
                setFromKey = fromStringToIntSet(key)
                [tile.removeCommon(setFromKey) for tile in self._tiles]
        
    def mapPossibleValues(self) -> None:
        for tile in self._tiles:
            for value in tile.possible_values:
                self._possible_values_map[value] = self._possible_values_map[value] + 1 if value in self._possible_values_map.keys() else 1

    def reverseMappedValues(self) -> None:
        for key, value in self._possible_values_map.items():
            if value not in self._possible_values_reverse_map.keys():
                self._possible_values_reverse_map[value] = set([key])
            else:
                self._possible_values_reverse_map[value].add(key)

    def findAndClearHiddenCommon(self) -> None:
        self.mapPossibleValues()
        # print('values mapped')
        self.reverseMappedValues()
        # print("Hidden pair reduction")
        for key, value in self._possible_values_reverse_map.items():
            combination_set: list[tuple[int]] = list(combinations(value, key))
            for combination in combination_set:
                counter: int = 0
                combination = set(combination)
                for tile in self._tiles:
                    counter += 1 if tile.findHidden(combination) else 0
                if counter == key:
                    [tile.clearHidden(combination) for tile in self._tiles]
        