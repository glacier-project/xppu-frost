from enum import Enum
from material import Material
from dataclasses import dataclass

class CCmdType(str, Enum):
    T_TO_END = "T_TO_END"
    T_TO_START = "T_TO_START"

@dataclass(frozen=True, order=True)
class ConveyorCmd:
    wp: Material
    cmd_type: CCmdType
