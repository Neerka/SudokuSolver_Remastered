from dataclasses import dataclass

@dataclass
class Column:
    """
    The column class has the following attributes:
    - id: the index of the column (0-8, left to right)
    - tiles: the tiles in the column
    """
    id: int
    values: list[int]
    tiles: list[int]

    def addTile(self, tile: int) -> None:
        """
        Add a tile to the column
        """
        self.tiles.append(tile)
        self.values.add(tile.value)