from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional
from column import Column
from row import Row
from group import Group

class Tile(BaseModel):
    """
    The tile class has the following attributes:
    - id: the index of the tile (0-80, left to right, top to bottom)
    - column: the column index of the tile
    - row: the row index of the tile
    - group: the group (a 3x3 subsquare on the board) index of the tile
    - value: the value of the tile, 0 if the value is unknown
    - possible_values: the possible values for the tile

    Rules for the currently possible values:
        1. for each two different tiles A and B, if A.column == B.column, then A.value != B.value
        2. for each two different tiles A and B, if A.row == B.row, then A.value != B.value
        3. for each two different tiles A and B, if A.group == B.group, then A.value != B.value
    """

    # Basic tile class to indicate a tile in the sudoku board
    id: int
    column: Optional[Column] = None
    row: Optional[Row] = None
    group: Optional[Group] = None
    value: Optional[int] = 0  # value for unknown tiles
    _possible_values: set[int] = PrivateAttr()
    
    def __init__(self, **data):
        super().__init__(**data)
        self._possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9} if self.value == 0 else {}

    @property
    def possible_values(self) -> set[int]:
        return self._possible_values

    def findInColumn(self) -> set[int]:
        """
        Find the possible values for the tile based on the column
        """
        return self._possible_values - self.column.values

    def findInRow(self) -> set[int]:
        """
        Find the possible values for the tile based on the row
        """
        return self._possible_values - self.row.values
    
    def findInGroup(self) -> set[int]:
        """
        Find the possible values for the tile based on the group
        """
        return self._possible_values - self.group.values
    
    def findPossibleValues(self) -> None:
        """
        Find the possible values for the tile based on the column, row, and group
        """
        result = self.findInColumn() & self.findInRow() & self.findInGroup()
        self._possible_values = result
    
    def updateValue(self) -> None:
        """
        Update the value of the tile based on the possible values
        """
        if len(self._possible_values) == 1:
            self.value = self._possible_values.pop()

    def findUniqueCandidatesInColumns(self) -> set[int]:
        """
        Find the possible values for the tile based on the column
        """
        temp = self._possible_values.copy()
        for tile in self.column.tiles:
            if tile.id != self.id:
                temp -= tile.possible_values
        return temp
    
    def findUniqueCandidatesInRows(self) -> set[int]:
        """
        Find the possible values for the tile based on the row
        """
        temp = self._possible_values.copy()
        for tile in self.row.tiles:
            if tile.id != self.id:
                temp -= tile.possible_values
        return temp
    
    def findUniqueCandidatesInGroups(self) -> set[int]:
        """
        Find the possible values for the tile based on the group
        """
        temp = self._possible_values.copy()
        for tile in self.group.tiles:
            if tile.id != self.id:
                temp -= tile.possible_values
        return temp
    
    def updateOnUniqueCandidates(self) -> None:
        """
        Updates the value of the tile based on the unique candidates in the column, row, and group
        """
        col = self.findUniqueCandidatesInColumns()
        row = self.findUniqueCandidatesInRows()
        group = self.findUniqueCandidatesInGroups()
        if len(col) == 1:
            self.value = col.pop()
        if len(row) == 1:
            self.value = row.pop()
        if len(group) == 1:
            self.value = group.pop()
    
    def update(self) -> None:
        """
        Update the possible values and the value of the tile
        """
        if self.value != 0:
            return
        self.findPossibleValues()
        self.updateValue()
        if self.value != 0:
            return
        self.updateOnUniqueCandidates()
        
        
        