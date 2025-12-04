from enum import Enum

class StampCmd(str, Enum):
    STAMP_LIGHT_P = "STAMP_LIGHT_P"
    STAMP_MEDIUM_P = "STAMP_MEDIUM_P"
    STAMP_HEAVY_P = "STAMP_HEAVY_P"
