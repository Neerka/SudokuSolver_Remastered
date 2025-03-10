import os

from sudokuBoard import Board
from tile import Tile
from pydantic import BaseModel, PrivateAttr

class BoardCreator(BaseModel):
    """
    The board processor class has the following attributes:
    - board: the SudokuBoard object
    - board_source: file from which the board is loaded
    """
    _board: Board = PrivateAttr(default=None)
    _board_source: str = PrivateAttr(default="")

    def __init__(self, board_source: str, **data):
        super().__init__(**data)
        self._board_source = board_source

    @property
    def board(self) -> Board:
        return self._board
    
    @board.setter
    def board(self, board: Board) -> None:
        self._board = board

    @property
    def board_source(self) -> str:
        return self._board_source
    
    @board_source.setter
    def board_source(self, board_source: str) -> None:
        self._board_source = board_source

    def createBoard(self, boardID: int) -> None:
        board = []
        tiles = []
        with open(self.board_source, "r") as source:
            for line in source:
                line = line.strip()
                for x in line:
                    x = int(x)
                    board.append(x)
        for i in range(len(board)):
            temp = Tile(id=i)
            if board[i] != 0:
                temp.value = board[i]
            # temp.value(board[i]) if board[i] != 0 else 0
            tiles.append(temp)
        self._board = Board(tiles, id=boardID)

    def solveBoard(self) -> bool:
        return self._board.solve()

    def lookAtTileValue(self, tileID: int) -> int:
        return self._board.lookAtTileValue(tileID)
    
    def lookAtTilePossibleValues(self, tileID: int) -> set[int]:
        return self._board.lookAtTilePossibleValues(tileID)