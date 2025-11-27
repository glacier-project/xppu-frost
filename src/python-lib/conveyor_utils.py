from enum import Enum
from material import Material
from dataclasses import dataclass

class CCmdType(str, Enum):
    T_TO_END = "T_TO_END"
    T_TO_START = "T_TO_START"

class LSCCmdType(str, Enum):
    T_TO_PAC = "T_TO_PAC"
    T_TO_RAMP_START = "T_TO_RAMP_START"
    T_TO_RAMP_MID = "T_TO_RAMP_MID"
    T_TO_END = CCmdType.T_TO_END.value
    T_TO_START = CCmdType.T_TO_START.value

@dataclass(frozen=True, order=True)
class ConveyorCmd:
    wp: Material
    cmd_type: CCmdType