from enum import StrEnum, auto

FLOAT_SIZE = 4
INT_SIZE = 4
FILE_FORMAT = "MSVD"
SIMPLE = 1e-10
ADVANCED = 1300
class Method(StrEnum):
    NUMPY = auto()
    SIMPLE = auto()
    ADVANCED = auto()