from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional
from column import Column
from row import Row
from group import Group
from tile import Tile

class Board(BaseModel):
    id: int
    _columns: list[Column] = PrivateAttr(default=[])
    _rows: list[Row] = PrivateAttr(default=[])
    _groups: list[Group] = PrivateAttr(default=[])

    def __init__(self, tiles: list[Tile], **data,):
        super().__init__(**data)
        for i in range(9):
            col = Column(id=i)
            row = Row(id=i)
            gro = Group(id=i)
            self._columns.append(col)
            self._rows.append(row)
            self._groups.append(gro)
        self.assignTiles(tiles)

    def assignTiles(self, tiles: list[Tile]) -> None:
        for tile in tiles:
            tileID = tile.id
            try:
                self._columns[tileID % 9].addTile(tile)
                self._rows[tileID // 9].addTile(tile)
                self._groups[(tileID // 9) // 3 * 3 + (tileID % 9) // 3].addTile(tile)
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"{e}: WTF YOU DO HERE???")
    
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

    def nakedPairs(self) -> None:
        for column in self._columns:
            column.redundantNormalCommonValues()
        for row in self._rows:
            row.redundantNormalCommonValues()
        for group in self._groups:
            group.redundantNormalCommonValues()

    def hiddenPairs(self) -> None:
        for column in self._columns:
            column.findAndClearHiddenCommon()
        for row in self._rows:
            row.findAndClearHiddenCommon()
        for group in self._groups:
            group.findAndClearHiddenCommon()

    def solve(self) -> None:
        try:
            counter: int = 0
            while True:
                self.findValues()
                self.nakedPairs()
                self.hiddenPairs()
                self.findUniqueValues()
                self.updateTiles()
                if self.checkSolved()[0]:
                    break
                elif not self.checkSolved()[0] and not self.checkSolved()[1]:
                    counter += 1
                if counter > 20:
                    break
        except Exception as e:
            print(f"{e}")
    
    def checkSolved(self) -> tuple[bool, bool]:
        for group in self._groups:
            if not group.checkGroup()[0] and not group.checkGroup()[1]:
                return False, False
            elif not group.checkGroup()[0]:
                return False, True
        return True, True
    
    def lookAtTileValue(self, tileID: int) -> int:
        idx: int = ((tileID // 9) // 3) * 3 + (tileID % 9) // 3 
        return self._groups[idx].lookAtTileValue(tileID)
    
    def lookAtTilePossibleValues(self, tileID: int) -> set[int]:
        idx: int = ((tileID // 9) // 3) * 3 + (tileID % 9) // 3
        return self._groups[idx].lookAtTilePossibleValues(tileID)


