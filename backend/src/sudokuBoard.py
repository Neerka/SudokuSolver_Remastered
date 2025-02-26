from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional
from column import Column
from row import Row
from group import Group
from tile import Tile

class Board(BaseModel):
    _instance: Optional["Board"] = PrivateAttr(default=None)

    # id: int
    _columns: list[Column] = Field(default_factory=list)
    _rows: list[Row] = Field(default_factory=list)
    _groups: list[Group] = Field(default_factory=list)

    def __init__(self, tiles: list[Tile], **data,):
        super().__init__(**data)
        if Board._instance is not None:
            raise ValueError("Board is a singleton")
        self._instance = self
        for i in range(9):
            self._columns.append(Column(id=i))
            self._rows.append(Row(id=i))
            self._groups.append(Group(id=i))
        self.assignTiles(self, tiles)

    def assignTiles(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            tileID = tile.id
            try:
                self._columns[tileID % 9].addTile(tile)
                self._rows[tileID // 9].addTile(tile)
                self._groups[(tileID // 9) // 3 * 3 + (tileID % 9) // 3].addTile(tile)
            except ValueError as e:
                print(e)
            except:
                print("WTF YOU DO HERE???")

    @classmethod
    def getInstance(cls, **data) -> "Board":
        if cls._instance is None:
            cls._instance = cls(**data)
        return cls._instance
    
    @property
    def columns(self) -> list[Column]:
        return self._columns
    
    @property
    def rows(self) -> list[Row]:
        return self._rows
    
    @property
    def groups(self) -> list[Group]:
        return self._groups
    
    @property
    def tiles(self) -> list[Tile]:
        return self._tiles
    
    def findValues(self) -> None:
        for column in self._columns:
            column.findValues()
        for row in self._rows:
            row.findValues()
        for group in self._groups:
            group.findValues()
    
    def findUniqueValues(self) -> None:
        for column in self._columns:
            column.findUniqueValues()
        for row in self._rows:
            row.findUniqueValues()
        for group in self._groups:
            group.findUniqueValues()

    def updateTiles(self) -> None:
        for group in self._groups:
            group.updateTiles()


