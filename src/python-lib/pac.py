from enum import Enum
from conveyor import CCmdType
from pa import PAPos

class PACCmdType(str, Enum):
    T_TO_PS_START = "T_TO_PS_START"
    T_TO_PS_END = "T_TO_PS_END"
    T_TO_END = CCmdType.T_TO_END.value
    T_TO_START = CCmdType.T_TO_START.value
    # Aliases
    T_TO_LSC = T_TO_START
    T_TO_SSC = T_TO_END
    PICK_FROM_POS1 = "PICK_FROM_POS1"
    PICK_FROM_POS2 = "PICK_FROM_POS2"
    PICK_FROM_POS3 = "PICK_FROM_POS3"
    PICK_FROM_POS4 = "PICK_FROM_POS4"
    PUTDOWN_TO_POS1 = "PUTDOWN_TO_POS1"
    PUTDOWN_TO_POS2 = "PUTDOWN_TO_POS2"
    PUTDOWN_TO_POS3 = "PUTDOWN_TO_POS3"
    PUTDOWN_TO_POS4 = "PUTDOWN_TO_POS4"

# Lookups so the conveyor can iterate over the four PA positions instead of
# spelling out one branch per position for every pick/putdown decision.
PICK_CMD_BY_POS = {
    PAPos.POS1: PACCmdType.PICK_FROM_POS1,
    PAPos.POS2: PACCmdType.PICK_FROM_POS2,
    PAPos.POS3: PACCmdType.PICK_FROM_POS3,
    PAPos.POS4: PACCmdType.PICK_FROM_POS4,
}

PUTDOWN_CMD_BY_POS = {
    PAPos.POS1: PACCmdType.PUTDOWN_TO_POS1,
    PAPos.POS2: PACCmdType.PUTDOWN_TO_POS2,
    PAPos.POS3: PACCmdType.PUTDOWN_TO_POS3,
    PAPos.POS4: PACCmdType.PUTDOWN_TO_POS4,
}

# Reverse lookups: which PA position (if any) a conveyor command refers to.
POS_BY_PICK_CMD = {cmd: pos for pos, cmd in PICK_CMD_BY_POS.items()}
POS_BY_PUTDOWN_CMD = {cmd: pos for pos, cmd in PUTDOWN_CMD_BY_POS.items()}
