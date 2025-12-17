from enum import Enum
from conveyor import CCmdType

class RFCCmdType(str, Enum):
    T_TO_PS_END = "T_TO_PS_END"
    T_TO_END = CCmdType.T_TO_END.value
    T_TO_START = CCmdType.T_TO_START.value
    # Aliases
    T_TO_LSC = T_TO_END
    T_TO_SSC = T_TO_START
