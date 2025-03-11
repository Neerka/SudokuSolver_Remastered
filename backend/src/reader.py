import cv2 as cv
import torch as tr


class Reader:
    """
    Reader class for extracting Sudoku data from screenshots.
    This singleton class is responsible for reading and processing screenshot data
    to extract the Sudoku grid information. It ensures only one instance exists
    throughout the application lifecycle to maintain consistent data processing.
    Attributes:
        _instance (Reader): Class variable holding the single instance of Reader.
        _initialized (bool): Flag to track whether the instance has been initialized.
    Methods:
        __new__(cls, *args, **kwargs): Ensures only one instance of Reader exists.
        __init__(): Initializes the Reader instance if not already initialized.
    """

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True