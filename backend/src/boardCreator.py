import os

from sudokuBoard import Board
from tile import Tile
class BoardCreator:
    """
    The board creator class as a singleton that creates and operates on Sudoku boards.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    def createBoard(self, board_source: str, boardID: int) -> Board:
        board_values = []
        tiles = []
        
        with open(board_source, "r") as source:
            for line in source:
                line = line.strip()
                for x in line:
                    x = int(x)
                    board_values.append(x)
                    
        for i in range(len(board_values)):
            temp = Tile(id=i)
            if board_values[i] != 0:
                temp.value = board_values[i]
            tiles.append(temp)
            
        return Board(tiles, id=boardID)

