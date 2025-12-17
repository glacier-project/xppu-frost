from enum import Enum
from conveyor import CCmdType

class SSCCmdType(str, Enum):
    T_TO_RFC = "T_TO_RFC"
    T_TO_END = CCmdType.T_TO_END.value
    T_TO_START = CCmdType.T_TO_START.value
