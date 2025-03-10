from pydantic import BaseModel, Field, PrivateAttr
import heapq
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
    
    
    def checkIfSolvable(self) -> bool:
        for item in self.groups:
            if not item.checkIfSolvable():
                return False
        for item in self.columns:
            if not item.checkIfSolvable():
                return False
        for item in self.rows:
            if not item.checkIfSolvable():
                return False
        return True
        
    def findBestTile(self) -> Tile:
        """
        Find the best candidate tile for the next solving step.
        This method searches for the empty tile with the fewest possible values.
        It uses the following strategy:
        1. If an empty tile with exactly one possible value is found, it returns that tile immediately.
        2. Otherwise, it returns the empty tile with the minimum number of possible values.
        This heuristic improves solving efficiency by working with the most constrained tiles first.
        Returns:
            Tile: The most constrained empty tile, or None if no empty tiles are found.
        """
        best_tile: Tile = None
        min_possibilities = 10

        [group.findValues() for group in self.groups]
        [column.findValues() for column in self.columns]
        [row.findValues() for row in self.rows]

        for group in self.groups:
            for tile in group.tiles:
                if tile.value == 0:
                    tile.findPossibleValues()
                    possibilities = len(tile.possible_values)

                    if possibilities == 1:
                        return tile
                    
                    if possibilities == 0:
                        return False

                    if 1 < possibilities < min_possibilities:
                        min_possibilities = possibilities
                        best_tile = tile
                    
        return best_tile

    def solveWithBacktracking(self) -> bool:
        """
        Solves the Sudoku board using a backtracking algorithm.
        This method attempts to solve the Sudoku puzzle by using a backtracking approach.
        It first checks if the board is solvable, then iteratively:
        1. Finds the best candidate tile (with fewest possible values)
        2. Tries each possible value for that tile
        3. Recursively attempts to solve the rest of the puzzle
        4. Backtracks if a solution cannot be found with the current configuration
        Returns:
            bool: True if the Sudoku puzzle was successfully solved, False otherwise
                    - Returns False if the board is not solvable
                    - Returns True when all tiles have been assigned valid values        
        """
        if not self.checkIfSolvable():
            return False
        
        best_tile = self.findBestTile()

        if best_tile is False:
            return False
        
        if best_tile is None:
            return True
        
        for value in best_tile.possible_values:
            best_tile.value = value

            if self.solveWithBacktracking():
                return True
            
            best_tile.value = 0

        return False
    
    def lookAtTileValue(self, tileID: int) -> int:
        for group in self.groups:
            try:
                result = group.lookAtTileValue(tileID)
            except ValueError:
                pass
        return result

    def solve(self) -> bool:
        return self.solveWithBacktracking()
