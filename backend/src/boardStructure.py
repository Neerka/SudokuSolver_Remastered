from pydantic import BaseModel, Field, PrivateAttr
from tile import Tile

class BoardStructure(BaseModel):
    id: int
    _type: str = PrivateAttr()
    _tiles: list[Tile] = PrivateAttr(default=[])

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