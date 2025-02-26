from pydantic import BaseModel, PrivateAttr
from itertools import combinations

class Tile(BaseModel):
    """
    The tile class has the following attributes:
    - id: the index of the tile (0-80, left to right, top to bottom)
    - value: the value of the tile, 0 if the value is unknown
    - possible_values: the possible values for the tile
    - column_values: the possible values of the tile, based on the column
    - row_values: the possible values of the tile, based on the row
    - group_values: the possible values of the tile, based on the group

    Rules for the possible values (in case someone didn't know how to play sudoku):
        1. for each two different tiles A and B, if A.column == B.column, then A.value != B.value
        2. for each two different tiles A and B, if A.row == B.row, then A.value != B.value
        3. for each two different tiles A and B, if A.group == B.group, then A.value != B.value
        a. Those tiles don't have column, row or group attributes. This description was just to explain the rules.

    Tile class has the following methods:
    - findInColumn: find the possible values for the tile based on the column
    - findInRow: find the possible values for the tile based on the row
    - findInGroup: find the possible values for the tile based on the group
    - findPossibleValues: find the possible values for the tile based on the column, row, and group
    - updateValue: update the value of the tile based on the possible values
    - findUniqueCandidatesInColumns: find the possible values for the tile based on the column
    - findUniqueCandidatesInRows: find the possible values for the tile based on the row
    - findUniqueCandidatesInGroups: find the possible values for the tile based on the group
    - updateOnUniqueCandidates: update the value of the tile based on the unique candidates in the column, row, and group
    - update: update the possible values and the value of the
    """

    # Basic tile class to indicate a tile in the sudoku board
    id: int
    _value: int = 0  # value for unknown tiles
    _possible_values: set[int] = PrivateAttr(default={1, 2, 3, 4, 5, 6, 7, 8, 9})

    # Sets of possible values based on the column, row, and group
    _column_values: set[int] = PrivateAttr(default=set())
    _row_values: set[int] = PrivateAttr(default=set())
    _group_values: set[int] = PrivateAttr(default=set())

    # Sets of unique possible values based on the column, row, and group (used for advanced solving)
    _unigue_column_values: set[int] = PrivateAttr(default=set())
    _unigue_row_values: set[int] = PrivateAttr(default=set())
    _unigue_group_values: set[int] = PrivateAttr(default=set())

    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, value: int) -> None:
        self._value = value
        self._possible_values = {}

    @property
    def possible_values(self) -> set[int]:
        return self._possible_values

    def findInColumn(self, values: set[int]) -> None:
        """
        Find the possible values for the tile based on the column
        """
        self._column_values = self._possible_values - set(values)

    def findInRow(self, values: set[int]) -> None:
        """
        Find the possible values for the tile based on the row
        """
        self._row_values = self._possible_values - set(values)
    
    def findInGroup(self, values: set[int]) -> None:
        """
        Find the possible values for the tile based on the group
        """
        self._group_values = self._possible_values - set(values)
    
    def findPossibleValues(self) -> None:
        """
        Find the possible values for the tile based on the column, row, and group
        """
        result = self._column_values & self._row_values & self._group_values
        self._possible_values = result
    
    def updateValue(self) -> None:
        """
        Update the value of the tile based on the possible values
        """
        if len(self._possible_values) == 1:
            self.value(self._possible_values.pop())
        elif len(self._possible_values) == 0:
            ValueError("Tile has no possible values")
        else:
            ValueError("Tile has multiple possible values")

    def findUniqueCandidatesInColumns(self, values: set[set[int]]) -> None:
        """
        Find the possible values for the tile based on the column
        """
        temp = self._possible_values.copy()
        selfProof = True   # This is used to avoid removing the tile's own possible values
        for subset in values:
            if subset == temp and selfProof:
                selfProof = not selfProof
            else:
                temp -= subset
        self._unigue_column_values = temp
    
    def findUniqueCandidatesInRows(self, values: set[set[int]]) -> None:
        """
        Find the possible values for the tile based on the row
        """
        temp = self._possible_values.copy()
        selfProof = True   # This is used to avoid removing the tile's own possible values
        for subset in values:
            if subset == temp and selfProof:
                selfProof = not selfProof
            else:
                temp -= subset
        self._unigue_row_values = temp
    
    def findUniqueCandidatesInGroups(self, values: set[set[int]]) -> None:
        """
        Find the possible values for the tile based on the group
        """
        temp = self._possible_values.copy()
        selfProof = True   # This is used to avoid removing the tile's own possible values
        for subset in values:
            if subset == temp and selfProof:
                selfProof = not selfProof
            else:
                temp -= subset
        self._unigue_group_values = temp
    
    def updateOnUniqueCandidates(self) -> None:
        """
        Updates the value of the tile based on the unique candidates in the column, row, and group
        """
        sets = [self._unigue_column_values, self._unigue_row_values, self._unigue_group_values]
        intersections = []

        for n in range(1,4):
            for combo in combinations(sets, n):
                temp = set.intersection(*combo)
                if temp:
                    intersections.append(temp)
        
        for intersection in intersections:
            if len(intersection) == 1:
                self.value(intersection.pop())
                return
        
        ValueError("Tile doesn't have unique possible values")

    def update(self) -> None:
        """
        Update the possible values and the value of the tile
        """
        self.findPossibleValues()
        try:
            self.updateValue()
        except ValueError:
            try:
                self.updateOnUniqueCandidates()
            except ValueError:
                pass
            except:
                print("You shouldn't be here (unique update)")
        except:
            print("You shouldn't be here (normal update)")
        
        