from enum import Enum
from conveyor import CCmdType

class LSCCmdType(str, Enum):
    T_TO_PAC = "T_TO_PAC"
    T_TO_RAMP_START = "T_TO_RAMP_START"
    T_TO_RAMP_MID = "T_TO_RAMP_MID"
    T_TO_END = CCmdType.T_TO_END.value
    T_TO_START = CCmdType.T_TO_START.value
