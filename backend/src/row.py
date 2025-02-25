from dataclasses import dataclass

@dataclass
class Row:
    """
    The row class has the following attributes:
    - id: the index of the row (0-8, left to right)
    - tiles: the tiles in the row
    """
    id: int
    values: list[int]
    tiles: list[int]

    def addTile(self, tile: int) -> None:
        """
        Add a tile to the row
        """
        self.tiles.append(tile)
        self.values.add(tile.value)