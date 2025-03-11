import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from boardCreator import BoardCreator

def test_sudokuCreator():
    board_src = "backend/test_resources/sample1.in"
    creator = BoardCreator()
    board = creator.createBoard(board_src, 0)

    values = []
    for line in open(board_src):
        line = line.strip()
        for item in line:
            item = int(item)
            values.append(item)

    assert board is not None
    for i in range(81):
        assert board.lookAtTileValue(i) == values[i]

    
